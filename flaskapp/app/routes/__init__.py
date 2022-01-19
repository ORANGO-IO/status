from flask import Blueprint, request,Response
import sys
from flask_expects_json import expects_json
from app.validations.serviceSchema import serviceSchema
from app.validations.jobSchema import jobSchema
from app.Controllers.serviceController import ServiceController
from app.Controllers.job import JobController
from app.Controllers.job_record import Job_record_controller

# Loading parent folder
sys.path.append('../app')

from app.services import lithocenter,postbaker
job_record_controller = Job_record_controller()
serviceController = ServiceController()
jobController = JobController()
services_routes = Blueprint('services_routes', __name__,
                        template_folder='templates',)

@services_routes.route('/lithocenter_frontend')
def service_lithocenter_frontend():    
    lithocenter.check_frontend()
    return 'Hello, this is status.orango.io a flask microservice'
    
@services_routes.route('/postbaker_frontend')
def service_postbaker_frontend():    
    postbaker.check_frontend()
    return 'Hello, this is status.orango.io a flask microservice'

@services_routes.route('/job',methods=['POST','GET'])
@expects_json(jobSchema, ignore_for=['GET'])
def job():
    if request.method == 'POST':
        req = request.get_json()
        return jobController.create(req.get('order'),req.get('url'),req.get('action'),req.get('actionValue'),req.get('serviceId'))
    return jobController.all()

@services_routes.route('/',methods = ['POST'])
@expects_json(serviceSchema)
def createService():
    req = request.get_json()
    return serviceController.create(req.get('name'))

@services_routes.route('/verify_service/<job_id>',methods=['POST'])
def create_job_record(job_id = None):
    if type(int(job_id)) == int:
        return job_record_controller.create(job_id)
    return Response('{"error":"job_id not is integer"}', status=404, mimetype='application/json')