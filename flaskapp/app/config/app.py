from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
import os

app = Flask(__name__,template_folder='../templates',static_folder='../static')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["FLASK_DB_SEEDS_PATH"] = "app/migrations/seeds.py"
app.config['TIMEZONE'] =  os.getenv("TIMEZONE")

db = SQLAlchemy(app)
Scss(app,static_dir="app/static/css",asset_dir="app/static/sass")
