from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class MenuItem(BaseModel):
    """MenuItem model"""
    
    __tablename__ = 'menu_items'

    name = Column(String, nullable=False)
    item_type = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    availability = Column(Boolean, default=True)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'),
                           nullable=False)
    order_id = Column(String(36), ForeignKey('order.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        """Initialize menu item"""
        super().__init__(*args, **kwargs)
