#!/usr/bin/env python
"""This module contains the base model for the application."""
#!/usr/bin/env python
"""This module contains the base model for the application."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy Base
Base = declarative_base()



class BaseModel(Base):
    """
    Base model that contains common fields for all tables.
    """
    __abstract__ = True  # Ensures no table is created for BaseModel

    id = Column(String(36), primary_key=True, unique=True, nullable=False,
    id = Column(String(36), primary_key=True, unique=True, nullable=False,
                default=lambda: str(uuid.uuid4()))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow,
    updated_at = Column(TIMESTAMP, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)
