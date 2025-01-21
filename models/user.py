from sqlalchemy import Column, String
from models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
