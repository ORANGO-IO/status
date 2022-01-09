from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder='../templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["FLASK_DB_SEEDS_PATH"] = "app/migrations/seeds.py"

db = SQLAlchemy(app)
