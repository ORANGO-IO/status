from app.services import lithocenter, postbaker
from flask import Blueprint, request, Response
import sys
from flask_expects_json import expects_json
from app.validations.serviceSchema import serviceSchema
from app.validations.jobSchema import jobSchema
from app.Controllers.serviceController import ServiceController
from app.Controllers.job import JobController
from app.Controllers.job_record import Job_record_controller
from app.Controllers.service_group import Service_Group_Controller
from app.Models.Job import Job

# Loading parent folder
sys.path.append('../app')

job_record_controller = Job_record_controller()
serviceController = ServiceController()
jobController = JobController()
service_group_controller = Service_Group_Controller()
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


@services_routes.route('/job', methods=['POST', 'GET'])
@expects_json(jobSchema, ignore_for=['GET'])
def job():
    if request.method == 'POST':
        req = request.get_json()
        return jobController.create(req.get('order'), req.get('url'), req.get('action'), req.get('actionValue'), req.get('serviceId'),req.get('description'))
    return jobController.all()


@services_routes.route('/', methods=['POST'])
@expects_json(serviceSchema)
def createService():
    req = request.get_json()
    return serviceController.create(req.get('name'), req.get('service_group_id'))

@services_routes.route('/teste/execute_jobs')
def executeTestAllJobs():
    jobs = Job.query.order_by(Job.order).all()
    array_response = []
    for job in jobs:
        response =job_record_controller.create(job.id)
        array_response.append(response)
    return "terminou"
    



@services_routes.route('/verify_service/<job_id>', methods=['POST'])
def create_job_record(job_id=None):
    if type(int(job_id)) == int:
        return job_record_controller.create(job_id)
    return Response('{"error":"job_id not is integer"}', status=404, mimetype='application/json')


@services_routes.route('/job_record')
def get_job_record():
    return job_record_controller.all()


@services_routes.route('/service_group', methods=['POST'])
def service_group():
    req = request.get_json()
    return service_group_controller.create(req.get('name'))
