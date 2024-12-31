from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Order(BaseModel):
    """
    Order model to store order details.
    """
    __tablename__ = 'order'

    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'),
                           nullable=False)
    # Store item list as a serialized string
    items = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # e.g., 'pending',
    # 'completed', 'cancelled'
    payment_details = Column(String, nullable=True)

    # Relationships
    user = relationship('User', backref='orders')
    restaurant = relationship('Restaurant', backref='orders')
