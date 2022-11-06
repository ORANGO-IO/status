from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss

settings = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///../services/sqlite3.db",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "FLASK_DB_SEEDS_PATH": "app/migrations/seeds.py"
}
app = Flask(__name__,template_folder='../templates',static_folder='../static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../services/sqlite3.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["FLASK_DB_SEEDS_PATH"] = "app/migrations/seeds.py"
print(app.config["SQLALCHEMY_DATABASE_URI"] )
db = SQLAlchemy(app)
Scss(app,static_dir="app/static/css",asset_dir="app/static/sass")

def create_app():
    app = Flask(__name__)

    app.config.update(settings)

    db.init_app(app)

    return app