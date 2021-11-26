from app.services import lithocenter

@app.route('/check_services')
def check_services():    
    lithocenter.check_frontend()
    return 'Hello, this is status.orango.io a flask microservice'