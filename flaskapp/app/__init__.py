from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import requests
from bs4 import BeautifulSoup

from app.routes import services_routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    parent = relationship("Service", back_populates="services")


class StatusRecord(db.Model):
    __tablename__ = 'status_records'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


@app.route('/')
def index():    
    ''' Aqui eu devo capturar os status e imagens '''
    return render_template('status.html')

app.register_blueprint(services_routes, url_prefix='/service')
