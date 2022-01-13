from app.services.db import db

from sqlalchemy.sql import func

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self
        
    @classmethod
    def find_by_name(cls, name):
        return Service.query.filter(Service.name == name).first()