from sqlalchemy import (
    Column,
    Integer,
    DECIMAL,
    ForeignKey,
    Enum,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.client import Client
from datetime import datetime


class Order(BaseModel, Base):
    """Order model"""

    __tablename__ = "orders"

    client_id = Column(
        String(60),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
    )
    status = Column(
        String(20), nullable=False, default="active"
    )  # active, completed, cancelled
    total_price = Column(
        DECIMAL(10, 2), nullable=False
    )  # Added total_price field
    order_date = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    def __init__(self, *args, **kwargs):
        """Initialize order"""
        super().__init__(*args, **kwargs)
