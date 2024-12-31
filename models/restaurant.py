from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Restaurant(BaseModel):
    """Restaurant model"""
    
    __tablename__ = 'restaurants'

    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)

    reviews = relationship("Review", back_populates="restaurant")
    menu_items = relationship("MenuItem", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")

    def __init__(self, *args, **kwargs):
        """Initialize restaurant"""
        super().__init__(*args, **kwargs)

