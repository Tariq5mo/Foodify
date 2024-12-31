#!/usr/bin/env python3
"""Client model module"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel



class Client(BaseModel):
    """Client model"""
    
    __tablename__ = 'clients'

    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize client"""
        super().__init__(*args, **kwargs)

# Test

# my_client = Client(username="Ahmed", id="Ahmed", email="ahmed@example.com",
#                 password_hash="hashedpassword")
    

# print("Created Model:", my_client)

# import models
# storage.__session.add(my_client)
# print("Model Saved:", my_client)
