from app.services.db import db
from sqlalchemy.sql import func

class StatusImage(db.Model):
    __tablename__ = 'status_images'

    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String,nullable=False)
    mime_type = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())