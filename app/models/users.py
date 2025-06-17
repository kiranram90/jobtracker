from app import db
from sqlalchemy import Column, Integer, Text, ForeignKey, String, UUID
from sqlalchemy import ForeignKey


class User(db.Model):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
