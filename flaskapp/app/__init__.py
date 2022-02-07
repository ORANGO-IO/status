from flask import render_template

from app.routes import services_routes
from app.services.db import app, db
from app.Controllers.job_record import Job_record_controller

job_record_controller = Job_record_controller()

@app.route('/')
def index():
    ''' Aqui eu devo capturar os status e imagens '''
    return render_template('status.html',json = job_record_controller.all())


@app.route('/details')
def details():
    return render_template('details.html',json = job_record_controller.all())


app.register_blueprint(services_routes, url_prefix='/service')
