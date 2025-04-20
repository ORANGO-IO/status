import typer
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


# Garante que "web" está no path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from web import create_app, db
from web.services.scheduler import process_crawler, process_request, process_capture
from web.models import Service, Task

app = typer.Typer()


@app.command()
def create_service(
    slug: str = typer.Option(..., prompt=True),
    name: str = typer.Option(..., prompt=True),
    description: str = typer.Option("", prompt=True),
):
    """Cria um novo serviço"""
    flask_app = create_app()
    with flask_app.app_context():
        service = Service(slug=slug, name=name, description=description)
        db.session.add(service)
        db.session.commit()
        typer.echo(f"✅ Serviço criado: {service.name} ({service.id})")


@app.command()
def create_task(
    name: str = typer.Option(..., prompt="Nome da task"),
    type: str = typer.Option(..., prompt="Tipo da task (crawler/request/capture/e2e)"),
    config_json: str = typer.Option(..., prompt="JSON de configuração da task"),
):
    """Cria uma nova task vinculada a um serviço existente"""

    flask_app = create_app()
    with flask_app.app_context():
        services = Service.query.order_by(Service.name).all()
        if not services:
            typer.echo("❌ Nenhum serviço encontrado.")
            raise typer.Exit()

        typer.echo("📋 Serviços disponíveis:")
        for idx, svc in enumerate(services, start=1):
            typer.echo(f"{idx}. {svc.name} (slug: {svc.slug})")

        selected_index = typer.prompt("Digite o número do serviço desejado", type=int)

        if selected_index < 1 or selected_index > len(services):
            typer.echo("❌ Número inválido.")
            raise typer.Exit()

        selected_service = services[selected_index - 1]

        # Valida e carrega o JSON informado
        try:
            config = json.loads(config_json)
        except json.JSONDecodeError as e:
            typer.echo(f"❌ JSON inválido: {e}")
            raise typer.Exit()

        task = Task(name=name, type=type, config=config, service_id=selected_service.id)
        db.session.add(task)
        db.session.commit()

        typer.echo(
            f"✅ Task '{task.name}' criada com sucesso para o serviço '{selected_service.name}'"
        )


@app.command()
def run_task(
    task_id: str = typer.Option(None, help="ID da task"),
    task_name: str = typer.Option(None, help="(Alternativa) Nome exato da task")
):
    """Executa uma task manualmente, atualiza status e salva resultado"""

    flask_app = create_app()
    with flask_app.app_context():
        task = None

        if task_id:
            task = Task.query.filter_by(id=task_id).first()
        elif task_name:
            task = Task.query.filter_by(name=task_name).first()
        else:
            # Lista interativa
            tasks = Task.query.order_by(Task.name).all()
            if not tasks:
                typer.echo("❌ Nenhuma task encontrada.")
                raise typer.Exit()

            typer.echo("📋 Tasks disponíveis:")
            for idx, t in enumerate(tasks, start=1):
                typer.echo(f"{idx}. {t.name} ({t.type}) — Serviço: {t.service.name}")

            selected_index = typer.prompt("Digite o número da task para executar", type=int)
            if selected_index < 1 or selected_index > len(tasks):
                typer.echo("❌ Índice inválido.")
                raise typer.Exit()
            task = tasks[selected_index - 1]

        if not task:
            typer.echo("❌ Task não encontrada.")
            raise typer.Exit()

        typer.echo(f"▶️ Executando task '{task.name}' do tipo '{task.type}'...")

        if task.type == "crawler":
            status, output = process_crawler(task, commit=False)
        elif task.type == "request":
            status, output = process_request(task, commit=False)
        elif task.type == "capture":
            status, output = process_capture(task, commit=False)
        else:
            typer.echo(f"❌ Tipo de task '{task.type}' não suportado.")
            raise typer.Exit()

        now = datetime.now(timezone.utc)
        task.last_status = status
        task.last_ran_at = now

        from web.models import TaskResult
        result = TaskResult(
            task_id=task.id,
            status=status,
            output=output,
            timestamp=now
        )
        db.session.add(result)
        db.session.commit()

        typer.echo(f"✅ Resultado salvo: {status.upper()}")
        typer.echo(f"📦 Saída: {output[:300]}")


if __name__ == "__main__":
    app()
