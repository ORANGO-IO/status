from app.services.db import db
from sqlalchemy.sql import func

class Status(db.Model):
    __tablename__ = 'status'

    id= db.Column(db.Integer,primary_key=True)
    value=db.Column(db.String,unique=True, nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

        return self
    
    @classmethod
    def find_by_username(cls, value):
        return Status.query.filter(Status.value == value).first()
    