from flask import Blueprint, request
import sys
from flask_expects_json import expects_json
from app.validations.serviceSchema import serviceSchema
from app.validations.jobSchema import jobSchema
from app.Controllers.serviceController import ServiceController
from app.Controllers.job import JobController

# Loading parent folder
sys.path.append('../app')

from app.services import lithocenter,postbaker

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

@services_routes.route('/job',methods=['POST'])
@expects_json(jobSchema)
def createJob():
    req = request.get_json()
    return jobController.create(req.get('order'),req.get('url'),req.get('action'),req.get('actionValue'),req.get('serviceId'))

@services_routes.route('/',methods = ['POST'])
@expects_json(serviceSchema)
def createService():
    req = request.get_json()
    return serviceController.create(req.get('name'))