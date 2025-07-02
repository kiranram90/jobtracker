from app.extensions import db
from sqlalchemy import Column, Integer, Text, ForeignKey, String, UUID
from sqlalchemy import ForeignKey
import uuid
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True,default=uuid.uuid4)
    email = Column(String, unique=True)
    password_hash = Column(String)
