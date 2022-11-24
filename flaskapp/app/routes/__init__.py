
from flask import Blueprint, request, Response
import sys
from flask_expects_json import expects_json
from app.validations.service_schema import service_schema
from app.validations.job_schema import job_schema
from app.Controllers.Job import JobController
from app.Controllers.JobRecord import JobRecordController
from app.Controllers.ServiceGroupController import ServiceGroupController
from app.Controllers.ServiceRecord import ServiceRecordController
from app.Models.Job import Job
from app.Controllers.ServiceController import ServiceController

# Loading parent folder
sys.path.append('../app')

job_record_controller = JobRecordController()
job_controller = JobController()
service_group_controller = ServiceGroupController()
service_record_controller = ServiceRecordController()
services_routes = Blueprint('services_routes', __name__,
                            template_folder='templates',)
service_controller = ServiceController()

@services_routes.route('/job', methods=['POST', 'GET'])
@expects_json(job_schema, ignore_for=['GET'])
def job():
    if request.method == 'POST':
        req = request.get_json()
        return job_controller.create(req.get('order'), req.get('url'), req.get('action'), req.get('actionValue'), req.get('serviceId'),req.get('description'))
    return job_controller.all()

@services_routes.route('/execute_all_jobs')
def executeTestAllJobs():
    jobs = Job.query.order_by(Job.order).all()
    array_response = []
    for job in jobs:
        response =job_record_controller.create(job.id)
        array_response.append(response)
    return Response(status=201)

@services_routes.route('/verify_service/<service_group_id>', methods=['POST'])
def create_job_record(service_group_id=None):
    if type(int(service_group_id)) == int:
        response = service_record_controller.create(service_group_id)
        return response
    return Response('{"error":"service_group_id not is integer"}', status=404, mimetype='application/json')

@services_routes.route("/service",methods=['POST'])
@expects_json(service_schema)
def service():
    req = request.get_json()
    return service_controller.create(req.get("name"),req.get("service_group_id"))
    
@services_routes.route('/job_record')
def get_job_record():
    return job_record_controller.all()

@services_routes.route('/job_record/<job_id>',methods=['POST'])
def job_record(job_id = None):
    if type(int(job_id)) == int:
        return job_record_controller.create(job_id)
    return Response('{"error":"job_id not is integer"}', status=404, mimetype='application/json')

@services_routes.route('/service_group', methods=['POST','GET'])
def service_group():
    if request.method == 'POST':
        req = request.get_json()
        return service_group_controller.create(req.get('name'))
    return service_group_controller.all()
