from app.config.app import db

from sqlalchemy.sql import func

class Screenshot(db.Model):
    __tablename__ = 'screenshots'

    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String,nullable=False)
    mime_type = db.Column(db.String,nullable=False)
    job_record_id = db.Column(db.Integer,db.ForeignKey('job_records.id'),nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def save(self):
        db.session.add(self)
        db.session.commit()

        return self