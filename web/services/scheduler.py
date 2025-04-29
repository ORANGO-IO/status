from apscheduler.schedulers.background import BackgroundScheduler
from web import db
from web.models import Task, TaskResult
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from web.services.run_playwright_script import run_playwright_script
from zoneinfo import ZoneInfo


def process_service_check(task, commit=True):
    status, output = run_playwright_script(task.config)

    if commit:
        save_task_result(task, status, output)

    return status, output


def process_request(task, commit=True):
    import requests

    try:
        response = requests.request(
            method=task.config.get("method", "GET"),
            url=task.config.get("url"),
            headers=task.config.get("headers", {}),
            json=task.config.get("body", {}),
        )
        status = "success" if response.ok else "error"
        output = f"Response: {response.status_code}"
    except Exception as e:
        status = "error"
        output = str(e)

    if commit:
        save_task_result(task, status, output)
    return status, output


def process_capture(task, commit=True):
    status, output = run_playwright_script(task.config)

    if commit:
        save_task_result(task, status, output)
    return status, output


def save_task_result(task, status, output):
    now = datetime.now(timezone.utc)

    # Atualiza task
    task.last_status = status
    task.last_ran_at = now

    result = TaskResult(task_id=task.id, status=status, output=output, timestamp=now)
    db.session.add(result)
    db.session.commit()


def run_task_batch(task_type):
    print(f"Executando tasks do tipo: {task_type}")
    tasks = Task.query.filter_by(type=task_type, active=True).all()
    for task in tasks:
        if task_type == "check":
            process_service_check(task)
        elif task_type == "request":
            process_request(task)
        elif task_type == "capture":
            process_capture(task)


def start_scheduler(app):
    scheduler = BackgroundScheduler(timezone=ZoneInfo("America/Sao_Paulo"))

    def job_wrapper(task_type):
        def job():
            with app.app_context():
                run_task_batch(task_type)

        return job

    scheduler.add_job(job_wrapper("check"), trigger="cron", hour=2, minute=0)
    scheduler.add_job(job_wrapper("request"), trigger="cron", hour=2, minute=0)
    scheduler.add_job(job_wrapper("capture"), trigger="cron", hour=2, minute=0)

    scheduler.start()
    print("⏰ APScheduler agendado para executar diariamente às 02:00")
