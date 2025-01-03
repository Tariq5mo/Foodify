from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base


class Review(Base):
    """Review model"""

    __tablename__ = "reviews"

    user_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    restaurant_id = Column(String(36), ForeignKey("restaurant.id"),
                           nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    client = relationship("Client", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")

    def __init__(self, *args, **kwargs):
        """Initialize review"""
        super().__init__(*args, **kwargs)
