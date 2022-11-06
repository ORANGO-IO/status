from app.config.app import db

from sqlalchemy.sql import func


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,  nullable=False)
    service_group_id = db.Column(db.Integer, db.ForeignKey(
        'service_groups.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    service_group = db.relationship('Service_group',
        backref=db.backref('services', lazy=True))
    
    # jobs = db.relationship('Job',
    #     backref=db.backref('service', lazy=True))
    

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    @classmethod
    def find_by_name(cls, name,id):
        return Service.query.filter(Service.name == name,Service.service_group_id == id).first()

    @classmethod
    def find_by_id(cls, id):
        return Service.query.get(id)
