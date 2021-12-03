from flask import Blueprint, render_template, abort
import sys

# Loading parent folder
sys.path.append('../app')

from app.services import lithocenter

services_routes = Blueprint('services_routes', __name__,
                        template_folder='templates')

@services_routes.route('/lithocenter_frontend')
def service_lithocenter_frontend():    
    lithocenter.check_frontend()
    return 'Hello, this is status.orango.io a flask microservice'