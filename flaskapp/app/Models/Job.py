from app.config.app import db

from sqlalchemy.sql import func

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer,nullable=False)
    url = db.Column(db.String,nullable=False)
    action = db.Column(db.String,nullable=True)
    description = db.Column(db.String,nullable=True)
    action_value = db.Column(db.String,nullable=True)
    service_id = db.Column(db.Integer,db.ForeignKey('services.id'),nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    service = db.relationship('Service',
        backref=db.backref('jobs', lazy=True))

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    @classmethod
    def find_by_id(cls,id):
        return Job.query.get(id)

    