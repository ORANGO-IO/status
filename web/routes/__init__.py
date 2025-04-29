from flask import Blueprint, render_template, jsonify
from web.models import Task
from web.schemas import TaskSchema
from web.services.auth import token_required  # onde estiver seu decorator
from sqlalchemy.orm import joinedload
from zoneinfo import ZoneInfo

main_routes = Blueprint("main", __name__)


@main_routes.route("/")
def index():
    tasks = Task.query.order_by(Task.last_status != "success", Task.name).all()
    return render_template(
        "index.html.j2", tasks=tasks, timezone=ZoneInfo("America/Sao_Paulo")
    )


from datetime import timedelta, datetime


def get_task_status_bars(task):
    today = datetime.now(ZoneInfo("America/Sao_Paulo")).date()
    days = [today - timedelta(days=i) for i in range(90)][::-1]

    bars = []
    for day in days:
        result = next((r for r in task.results if r.timestamp.date() == day), None)

        if not result:
            color = "gray"
            timestamp = None
        else:
            timestamp = result.timestamp
            if result.status == "success":
                color = "green"
            elif result.status == "warning":
                color = "yellow"
            else:
                color = "red"

        bars.append({
            "timestamp": timestamp,
            "color": color,
        })

    return bars


@main_routes.route("/details/<task_id>")
def task_details(task_id):
    task = (
        Task.query.options(joinedload(Task.service), joinedload(Task.results))
        .filter_by(id=task_id)
        .first()
    )
    if not task:
        return "Task não encontrada", 404

    status_bars = get_task_status_bars(task)
    return render_template(
        "details.html.j2",
        task=task,
        status_bars=status_bars,
        timezone=ZoneInfo("America/Sao_Paulo"),
    )


@main_routes.route("/<service_slug>/")
def service_status(service_slug):
    tasks = (
        Task.query.join(Task.service)
        .filter_by(slug=service_slug)
        .order_by(Task.last_status != "success", Task.name)
        .all()
    )
    if not tasks:
        return "Serviço não encontrado", 404
    return render_template(
        "index.html.j2", tasks=tasks, timezone=ZoneInfo("America/Sao_Paulo")
    )


@main_routes.route("/service/<service_id>/task", methods=["GET"])
@main_routes.route("/service/<service_id>/task/<task_id>", methods=["GET"])
@token_required
def get_task(service_id, task_id):
    task = (
        Task.query.filter_by(id=task_id, service_id=service_id)
        .options(joinedload(Task.results))
        .first()
    )
    if not task:
        return jsonify(error="Task não encontrada"), 404

    # Ordenar resultados manualmente (opcional: limitar os últimos 5)
    task.results = sorted(task.results, key=lambda r: r.timestamp, reverse=True)[:5]

    return jsonify(task=TaskSchema.model_validate(task).model_dump())
