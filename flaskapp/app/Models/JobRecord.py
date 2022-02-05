from app.services.db import db

from sqlalchemy.sql import func

class JobRecord(db.Model):
    __tablename__ = 'job_records'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer,db.ForeignKey('jobs.id'),nullable=False)
    status_id = db.Column(db.Integer,db.ForeignKey('job_record_status.id'),nullable=False)
    time_spent_in_sec = db.Column(db.Integer,nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    status = db.relationship('JopRecordStatus',backref=db.backref('job_record',lazy=True))
    job = db.relationship('Job',backref=db.backref('job_record',lazy=True))
    
    def save(self):
        db.session.add(self)
        db.session.commit()

        return self