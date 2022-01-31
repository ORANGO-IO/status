from app.services.db import db

from sqlalchemy.sql import func


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    service_group_id = db.Column(db.Integer, db.ForeignKey(
        'service_groups.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    service_group = db.relationship('Service_group',
                                    backref=db.backref('job', lazy=True))

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    @classmethod
    def find_by_name(cls, name):
        return Service.query.filter(Service.name == name).first()

    @classmethod
    def find_by_id(cls, id):
        return Service.query.get(id)
