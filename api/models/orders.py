from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..dependencies.database import Base


class OrderType(enum.Enum):
    DINE_IN = "dine_in"
    TAKEOUT = "takeout"
    DELIVERY = "delivery"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    status = Column(String(50), nullable=False, default="pending")
    order_type = Column(Enum(OrderType), nullable=False, default=OrderType.DINE_IN)

    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")