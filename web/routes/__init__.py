from flask import Blueprint, render_template, jsonify, request
from web.models import Task
from sqlalchemy.orm import joinedload

main_routes = Blueprint("main", __name__)

@main_routes.route("/")
def index():
    # Busca todas as tarefas com o serviço relacionado
    tasks = Task.query.options(joinedload(Task.service)).all()
    return render_template("index.html.j2", tasks=tasks)

@main_routes.route("/task", methods=["GET"])
def get_tasks():
    task_id = request.args.get("id")
    service_id = request.args.get("service_id")

    query = Task.query

    if task_id:
        task = query.filter_by(id=task_id).first()
        return jsonify(task=task_to_dict(task)) if task else jsonify(error="Task not found"), 404

    if service_id:
        query = query.filter_by(service_id=service_id)

    tasks = query.all()
    return jsonify(tasks=[task_to_dict(t) for t in tasks])


def task_to_dict(task):
    return {
        "id": task.id,
        "name": task.name,
        "type": task.type,
        "active": task.active,
        "last_status": task.last_status,
        "last_ran_at": task.last_ran_at.isoformat() if task.last_ran_at else None,
        "config": task.config,
        "service_id": task.service_id,
    }