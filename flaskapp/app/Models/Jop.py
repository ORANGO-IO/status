from app.services.db import db

from sqlalchemy.sql import func

class Jop(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer,nullable=False)
    url = db.Column(db.Integer,nullable=False)
    action = db.Column(db.Integer,nullable=True)
    action_value = db.Column(db.Integer,nullable=True)
    service_id = db.Column(db.Integer,db.ForeignKey('service.id'),nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def save(self):
        db.session.add(self)
        db.session.commit()

        return self
