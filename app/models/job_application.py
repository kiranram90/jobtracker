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
    status = Column(String(50), default='applied')
    notes = Column(Text)
    created_at = Column(datetime)
    