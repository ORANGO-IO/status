from app.services.db import db
from sqlalchemy.sql import func

class Status(db.Model):
    __tablename__ = 'status'

    id= db.column(db.Integer,primary_key = True)
    value=db.column(db.Integer,primary_key=True)