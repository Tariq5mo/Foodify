from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Order(BaseModel):
    """Order model"""
    
    __tablename__ = 'orders'

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('pending', 'completed', name='order_status'), default='pending')

    client = relationship("Client", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete")

    def __init__(self, *args, **kwargs):
        """Initialize order"""
        super().__init__(*args, **kwargs)
