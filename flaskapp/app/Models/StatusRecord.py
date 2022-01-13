from app.services.db import db

from sqlalchemy.sql import func

class StatusRecord(db.Model):
    __tablename__ = 'status_records'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer,db.ForeignKey('services.id'),nullable=False)
    status_id = db.Column(db.Integer,db.ForeignKey('status.id'),nullable=False)
    image_id = db.Column(db.Integer,db.ForeignKey('status_images.id'),nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def save(self):
        db.session.add(self)
        db.session.commit()

        return self
