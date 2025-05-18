import typer
import json
import sys
import secrets
from datetime import datetime, timezone, timedelta
from pathlib import Path


# Garante que "web" está no path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from web import create_app, db
from web.services.scheduler import (
    process_service_check,
    process_request,
    process_capture,
)
from web.services.crypto_utils import encrypt_password
from web.models import Service, Task, TaskResult
from web.services.utils import now_utc

app = typer.Typer()


def _execute_and_save(task):
    """Executa uma task, atualiza status e salva o resultado."""
    typer.echo(f"▶️ Executando task '{task.name}' do tipo '{task.type}'...")
    if task.type == "check":
        status, output = process_service_check(task, commit=False)
    elif task.type == "request":
        status, output = process_request(task, commit=False)
    elif task.type == "capture":
        status, output = process_capture(task, commit=False)
    else:
        typer.echo(f"❌ Tipo de task '{task.type}' não suportado.")
        return

    now = datetime.now(timezone.utc)
    task.last_status = status
    task.last_ran_at = now

    result = TaskResult(task_id=task.id, status=status, output=output, timestamp=now)
    db.session.add(result)
    db.session.commit()

    typer.echo(f"✅ Resultado salvo: {status.upper()}")
    typer.echo(f"📦 Saída: {str(output)[:300]}")


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
    description: str = typer.Option("", prompt="Descrição da task"),
    type: str = typer.Option(..., prompt="Tipo da task (check/request/capture/e2e)"),
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

        task = Task(
            name=name,
            description=description,
            type=type,
            config=config,
            service_id=selected_service.id,
        )
        db.session.add(task)
        db.session.commit()

        typer.echo(
            f"✅ Task '{task.name}' criada com sucesso para o serviço '{selected_service.name}'"
        )


@app.command()
def run_task(
    task_id_or_name: str = typer.Argument(None, help="ID da task ou nome da task"),
):
    """Executa uma task manualmente"""
    flask_app = create_app()
    with flask_app.app_context():
        # Seleção da task
        task = None
        if task_id_or_name:
            task = (
                Task.query.filter_by(id=task_id_or_name).first()
                or Task.query.filter_by(name=task_id_or_name).first()
            )
        if not task:
            tasks = Task.query.order_by(Task.name).all()
            if not tasks:
                typer.echo("❌ Nenhuma task encontrada.")
                raise typer.Exit()
            typer.echo("📋 Tasks disponíveis:")
            for idx, t in enumerate(tasks, start=1):
                typer.echo(f"{idx}. {t.name} ({t.type}) — Serviço: {t.service.name}")
            selected_index = typer.prompt(
                "Digite o número da task para executar", type=int
            )
            if selected_index < 1 or selected_index > len(tasks):
                typer.echo("❌ Índice inválido.")
                raise typer.Exit()
            task = tasks[selected_index - 1]

        if not task:
            typer.echo("❌ Task não encontrada.")
            raise typer.Exit()

        _execute_and_save(task)


@app.command()
def create_token():
    """Cria um novo token de acesso vinculado a um serviço (ou global para todos os serviços)"""

    flask_app = create_app()
    with flask_app.app_context():
        services = Service.query.order_by(Service.name).all()
        typer.echo("📋 Serviços disponíveis:")
        for idx, svc in enumerate(services, start=1):
            typer.echo(f"{idx}. {svc.name} (slug: {svc.slug})")
        typer.echo("0. (Acesso global a todos os serviços)")

        selected_index = typer.prompt("Escolha o número do serviço ou 0", type=int)
        if selected_index == 0:
            selected_service_id = None
        elif selected_index < 0 or selected_index > len(services):
            typer.echo("❌ Número inválido.")
            raise typer.Exit()
        else:
            selected_service_id = services[selected_index - 1].id

        typer.echo("📦 Tipos de token:")
        typer.echo("1. api      → Para APIs externas autenticadas")
        typer.echo("2. webhook  → Para receber eventos externos")
        typer.echo("3. cli      → Uso interno do Typer ou ferramentas")
        typer.echo("4. master   → Acesso total (cuidado!)")

        type_choice = typer.prompt("Escolha o tipo de token", type=int)
        type_map = {1: "api", 2: "webhook", 3: "cli", 4: "master"}
        token_system = type_map.get(type_choice)

        if not token_system:
            typer.echo("❌ Tipo inválido.")
            raise typer.Exit()

        # Gerar token seguro
        raw_token = secrets.token_urlsafe(32)
        now = now_utc()

        from web.models import Credential

        credential = Credential(
            secret=raw_token,
            role="token",
            system=token_system,
            service_id=selected_service_id,
            created_at=now,
            expires_at=now + timedelta(days=365),
        )
        db.session.add(credential)
        db.session.commit()

        typer.echo("✅ Token criado com sucesso!")
        typer.echo(f"🔐 Token: {raw_token}")
        if selected_service_id:
            typer.echo(f"🔗 Serviço: {services[selected_index - 1].name}")
        else:
            typer.echo("🌐 Token com acesso GLOBAL (todos os serviços)")
        typer.echo(f"🔖 Tipo: {token_system}")


@app.command()
def create_password():
    """Cria um novo credential com role=password (senha criptografada)"""

    flask_app = create_app()
    with flask_app.app_context():
        services = Service.query.order_by(Service.name).all()
        typer.echo("📋 Serviços disponíveis:")
        for idx, svc in enumerate(services, start=1):
            typer.echo(f"{idx}. {svc.name} (slug: {svc.slug})")
        typer.echo("0. (Não vincular a serviço)")

        selected_index = typer.prompt("Escolha o número do serviço ou 0", type=int)
        if selected_index == 0:
            selected_service_id = None
        elif selected_index < 0 or selected_index > len(services):
            typer.echo("❌ Número inválido.")
            raise typer.Exit()
        else:
            selected_service_id = services[selected_index - 1].id

        # Perguntar se quer gerar senha forte ou digitar uma
        choice = typer.prompt(
            "Deseja gerar uma senha forte automaticamente? [s/N]", default="N"
        )
        if choice.lower() == "s":
            import secrets, string

            alphabet = string.ascii_letters + string.digits + string.punctuation
            password = "".join(secrets.choice(alphabet) for _ in range(12))
            typer.echo(f"🔑 Senha gerada: {password}")
        else:
            password = typer.prompt(
                "Digite a senha", hide_input=True, confirmation_prompt=True
            )

        encrypted = encrypt_password(password)
        now = now_utc()

        from web.models import Credential

        credential = Credential(
            secret=encrypted,
            role="password",
            system="external",  # Ou outro valor, dependendo do seu enum
            service_id=selected_service_id,
            created_at=now,
            expires_at=now + timedelta(days=365),
        )
        db.session.add(credential)
        db.session.commit()
        typer.echo("✅ Credential do tipo password criado com sucesso!")
        typer.echo("🔗 UUID: " + str(credential.uuid))
        typer.echo(f"🔑 Senha original: {password}")
        typer.echo(f"🗝️  Senha criptografada (banco): {encrypted}")


# Função para executar todas as tasks de um serviço manualmente
@app.command()
def run_service(
    service_id_or_slug: str = typer.Argument(None, help="ID ou slug do serviço"),
):
    """Executa todas as tasks de um serviço manualmente"""

    flask_app = create_app()
    with flask_app.app_context():
        # Seleção do serviço
        service = (
            Service.query.filter(
                (Service.id == service_id_or_slug)
                | (Service.slug == service_id_or_slug)
            ).first()
            if service_id_or_slug
            else None
        )
        if not service:
            services = Service.query.order_by(Service.name).all()
            if not services:
                typer.echo("❌ Nenhum serviço encontrado.")
                raise typer.Exit()
            typer.echo("📋 Serviços disponíveis:")
            for idx, svc in enumerate(services, start=1):
                typer.echo(f"{idx}. {svc.name} (slug: {svc.slug})")
            selected_index = typer.prompt(
                "Digite o número do serviço para executar", type=int
            )
            if selected_index < 1 or selected_index > len(services):
                typer.echo("❌ Índice inválido.")
                raise typer.Exit()
            service = services[selected_index - 1]

        typer.echo(f"▶️ Executando todas as tasks do serviço '{service.name}'...")
        tasks = (
            Task.query.filter_by(service_id=service.id, active=True)
            .order_by(Task.name)
            .all()
        )
        if not tasks:
            typer.echo("⚠️ Nenhuma task ativa encontrada para este serviço.")
            raise typer.Exit()

        for task in tasks:
            _execute_and_save(task)


if __name__ == "__main__":
    app()
