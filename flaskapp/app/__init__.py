from flask import render_template, jsonify

from app.routes import services_routes
from app.config.app import app, db
from app.Controllers.jobRecord import JobRecordController


job_record_controller = JobRecordController()


@app.route('/')
def index():
    return render_template('status.html', json=job_record_controller.all())


@app.route('/cron_job_test')
def cron_job_test():
    app.logger.info("Testing cron route")
    response = jsonify(success=True)
    response.status_code = 200
    return response


@app.route('/details/<service_id>')
def details(service_id=None):
    if type(int(service_id)) == int:
        return render_template('details.html', json=job_record_controller.get_job_records_by_service(service_id=service_id))


app.register_blueprint(services_routes, url_prefix='/api')
