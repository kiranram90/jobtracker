from sqlalchemy import Column, Integer, String
from app import db
from sqlalchemy import Column, Integer, Text, ForeignKey, UUID


class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    user_id = Column(UUID, ForeignKey('user.id'))
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    