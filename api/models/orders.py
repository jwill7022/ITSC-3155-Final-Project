from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Enum, func, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import secrets
from ..dependencies.database import Base


class OrderType(enum.Enum):
    DINE_IN = "dine_in"
    TAKEOUT = "takeout"
    DELIVERY = "delivery"

class StatusType(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    AWAITING_PICKUP = "awaiting_pickup"
    OUT_FOR_DELIVERY = "out_for_delivery"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    tracking_number = Column(String(20), unique=True, nullable=True, index=True)
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    description = Column(String(300))
    status = Column(Enum(StatusType), nullable=False, default=StatusType.PENDING)
    order_type = Column(Enum(OrderType), nullable=False, default=OrderType.DINE_IN)

    #Cost variables
    subtotal = Column(Numeric(10, 2), nullable=True)
    tax_amount = Column(Numeric(10, 2), nullable=True)
    discount_amount = Column(Numeric(10, 2), nullable=True, default=0)
    total_amount = Column(Numeric(10, 2), nullable=True)
    promotion_code = Column(String(50), nullable=True)

    guest_name = Column(String(100), nullable=True)
    guest_phone = Column(String(20), nullable=True)
    guest_email = Column(String(100), nullable=True)

    estimated_completion = Column(DATETIME, nullable=True)

    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()

    @staticmethod
    def generate_tracking_number():
        return f"ORD{secrets.token_hex(4).upper()}"