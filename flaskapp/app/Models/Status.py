from app.services.db import db
from sqlalchemy.sql import func

class Status(db.Model):
    __tablename__ = 'status'

    id= db.Column(db.Integer,primary_key=True)
    value=db.Column(db.String,unique=True, nullable=False)