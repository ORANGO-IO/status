import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    TIMEZONE = os.getenv("TIMEZONE")
    TEMPLATE_FOLDER = "./templates"
    STATIC_FOLDER = "./static"