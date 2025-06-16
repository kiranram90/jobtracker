from sqlalchemy import Column, Integer, String
from app import db
from sqlalchemy import Column, Integer, Text, ForeignKey, UUID
from datetime import datetime


class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    user_id = Column(UUID, ForeignKey('user.id'))
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    posting= Column(String, nullable=False)
    status = db.Column(db.String(50), default='applied')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    