from app.services.db import db

from sqlalchemy.sql import func

class StatusRecord(db.Model):
    __tablename__ = 'status_records'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(80), nullable=False)
    service_id = db.Column(db.Integer,db.ForeignKey('services.id'),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

