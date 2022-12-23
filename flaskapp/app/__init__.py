from flask import render_template, jsonify

from app.routes import services_routes
from app.config.app import app, db
from app.Controllers.JobRecord import JobRecordController
from flask_paginate import Pagination, get_page_parameter

from flask import request
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
        search = False
        q = request.args.get('q')
        if q:
            search = True
        page = request.args.get(get_page_parameter(), type=int, default=1)
        json = job_record_controller.get_job_records_by_service(service_id=service_id,page=page)
        pagination = Pagination(page=page, total=json["count"], css_framework='foundation',search=search, record_name='json.jobs_records')
        return render_template('details.html', json=json,pagination=pagination)


app.register_blueprint(services_routes, url_prefix='/api')
