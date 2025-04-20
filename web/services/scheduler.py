from apscheduler.schedulers.background import BackgroundScheduler
from web import db
from web.models import Task, TaskResult
from datetime import datetime, timezone

def process_crawler(task):
    # Lógica para verificar se o site está online (exemplo básico)
    import requests
    try:
        response = requests.get(task.config.get("url"), timeout=5)
        status = "success" if response.status_code == 200 else "error"
        output = f"Status {response.status_code}"
    except Exception as e:
        status = "error"
        output = str(e)

    save_task_result(task, status, output)

def process_request(task):
    # Lógica para verificar se API está respondendo corretamente
    import requests
    try:
        response = requests.request(
            method=task.config.get("method", "GET"),
            url=task.config.get("url"),
            headers=task.config.get("headers", {}),
            json=task.config.get("body", {})
        )
        status = "success" if response.ok else "error"
        output = f"Response: {response.status_code}"
    except Exception as e:
        status = "error"
        output = str(e)

    save_task_result(task, status, output)

def process_capture(task):
    # Lógica de captura de string (ex: versão via XPath, não implementado aqui)
    status = "success"
    output = "simulated-capture-result"
    save_task_result(task, status, output)

def save_task_result(task, status, output):
    now = datetime.now(timezone.utc)

    # Atualiza task
    task.last_status = status
    task.last_ran_at = now

    result = TaskResult(
        task_id=task.id,
        status=status,
        output=output,
        timestamp=now
    )
    db.session.add(result)
    db.session.commit()

def run_task_batch(task_type):
    print(f"Executando tasks do tipo: {task_type}")
    tasks = Task.query.filter_by(type=task_type, active=True).all()
    for task in tasks:
        if task_type == "crawler":
            process_crawler(task)
        elif task_type == "request":
            process_request(task)
        elif task_type == "capture":
            process_capture(task)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: run_task_batch("crawler"), "interval", seconds=60)
    scheduler.add_job(lambda: run_task_batch("request"), "interval", seconds=90)
    scheduler.add_job(lambda: run_task_batch("capture"), "interval", seconds=180)
    scheduler.start()
    print("⏰ APScheduler started")