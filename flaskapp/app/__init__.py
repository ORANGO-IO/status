from flask import render_template

from app.routes import services_routes
from app.services.db import app, db

# !Temporário
db.create_all()
# app = create_app()


@app.route('/')
def index():
    ''' Aqui eu devo capturar os status e imagens '''
    return render_template('status.html')


@app.route('/details')
def details():
    return render_template('details.html')


app.register_blueprint(services_routes, url_prefix='/service')
