from sqlalchemy import Column, Integer, String
from app import db
from sqlalchemy import Column, Integer, Text, ForeignKey, UUID
from datetime import datetime
import uuid


class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID,ForeignKey('users.id'), nullable=False)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    posting= Column(String, nullable=False)
    status = Column(String(50), default='applied')
    notes = Column(Text)
    created_at = Column(db.DateTime)

    user = db.relationship('User', backref='applications')
    