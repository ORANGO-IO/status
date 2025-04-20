from flask import Blueprint, render_template, jsonify
from web.models import Task
from web.schemas import TaskSchema
from web.services.auth import token_required  # onde estiver seu decorator
from sqlalchemy.orm import joinedload
from zoneinfo import ZoneInfo

main_routes = Blueprint("main", __name__)

@main_routes.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html.j2", tasks=tasks, timezone=ZoneInfo("America/Sao_Paulo"))


@main_routes.route("/service/<service_id>/task", methods=["GET"])
@main_routes.route("/service/<service_id>/task/<task_id>", methods=["GET"])
@token_required
def get_task(service_id, task_id):
    task = (
        Task.query
        .filter_by(id=task_id, service_id=service_id)
        .options(joinedload(Task.results))
        .first()
    )
    if not task:
        return jsonify(error="Task não encontrada"), 404

    # Ordenar resultados manualmente (opcional: limitar os últimos 5)
    task.results = sorted(task.results, key=lambda r: r.timestamp, reverse=True)[:5]

    return jsonify(task=TaskSchema.model_validate(task).model_dump())