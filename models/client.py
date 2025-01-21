#!/usr/bin/env python3
"""Client model module"""
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from flask_login import UserMixin

# from app import login_manager


class Client(BaseModel, Base, UserMixin):
    """Client model"""

    __tablename__ = "clients"

    username = Column(String(70), nullable=False)
    address = Column(String(70), nullable=False)  # Combined address field
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    phone = Column(String(20), nullable=True)
    delivery_instructions = Column(String(500), nullable=True)
    contact_name = Column(String(100), nullable=True)

    reviews = relationship(
        "Review", back_populates="client", cascade="all, delete-orphan"
    )
    orders = relationship(
        "Order", back_populates="client", cascade="all, delete-orphan"
    )

    def __init__(self, *args, **kwargs):
        """Initialize client"""
        super().__init__(*args, **kwargs)

    def update(self, **kwargs):
        """Update client attributes"""
        allowed_fields = ["email", "address"]
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        self.save()
