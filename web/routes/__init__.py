from flask import Blueprint, render_template, jsonify
from web.models import Task
from web.schemas import TaskSchema
from web.services.auth import token_required  # onde estiver seu decorator
from sqlalchemy.orm import joinedload

main_routes = Blueprint("main", __name__)

@main_routes.route("/")
def index():
    # Busca todas as tarefas com o serviço relacionado
    tasks = Task.query.options(joinedload(Task.service)).all()
    return render_template("index.html.j2", tasks=tasks)


@main_routes.route("/service/<service_id>/task", methods=["GET"])
@main_routes.route("/service/<service_id>/task/<task_id>", methods=["GET"])
@token_required
def get_tasks(service_id, task_id=None):
    query = Task.query.filter_by(service_id=service_id)

    if task_id:
        task = query.filter_by(id=task_id).first()
        if not task:
            return jsonify(error="Task não encontrada"), 404
        return jsonify(task=TaskSchema.model_validate(task).model_dump())

    tasks = query.all()
    return jsonify(tasks=[TaskSchema.model_validate(t).model_dump() for t in tasks])