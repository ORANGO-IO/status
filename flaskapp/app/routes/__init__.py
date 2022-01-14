from flask import Blueprint, request
import sys

from app.Controllers.serviceController import ServiceController

# Loading parent folder
sys.path.append('../app')

from app.services import lithocenter,postbaker

serviceController = ServiceController()
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
@services_routes.route('/service',methods = ['POST'])
def createService():
    req = request.get_json()
    return serviceController.create(req.get('name'))