from app.config.app import db

from sqlalchemy.sql import func

class ServiceGroup(db.Model):
    __tablename__ = 'service_groups'

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
        return ServiceGroup.query.filter(ServiceGroup.name == name).first()
    
    @classmethod
    def find_by_id(cls,id):
        return ServiceGroup.query.get(id)