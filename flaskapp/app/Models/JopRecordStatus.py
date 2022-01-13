from app.services.db import db
from sqlalchemy.sql import func

class JopRecordStatus(db.Model):
    __tablename__ = 'job_record_status'

    id= db.Column(db.Integer,primary_key=True)
    value=db.Column(db.String,unique=True, nullable=False)
    description=db.Column(db.String,unique=True, nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

        return self
    
    @classmethod
    def find_by_name(cls, value):
        return JopRecordStatus.query.filter(JopRecordStatus.value == value).first()
    