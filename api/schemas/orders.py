from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum
from .order_details import OrderDetail
from .payments import Payment


class OrderType(str, Enum):
    DINE_IN = "dine_in"
    TAKEOUT = "takeout"
    DELIVERY = "delivery"

class StatusType(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    AWAITING_PICKUP = "awaiting_pickup"
    OUT_FOR_DELIVERY = "out_for_delivery"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class OrderBase(BaseModel):
    customer_id: Optional[int] = None #Optional in case of guest order
    description: Optional[str] = None
    status: StatusType = StatusType.PENDING
    order_type: OrderType = OrderType.DINE_IN


class OrderCreate(OrderBase):
    #For guest orders
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None

class GuestOrderCreate(BaseModel):
    guest_name: str
    guest_phone: str
    guest_email: Optional[str] = None
    description: Optional[str] = None
    order_type: OrderType = OrderType.DINE_IN
    promotion_code: Optional[str] = None


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[StatusType] = None
    order_type: Optional[OrderType] = None
    promotion_code: Optional[str] = None


class Order(OrderBase):
    id: int
    tracking_number: str
    order_date: Optional[datetime] = None
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    total_amount: Optional[float] = None
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_email: Optional[str] = None
    order_details: Optional[list[OrderDetail]] = None
    payment: Optional[Payment] = None

    class ConfigDict:
        from_attributes = True


class OrderTrack(BaseModel):
    id: int
    tracking_number: str
    status: StatusType
    order_date: datetime
    order_type: OrderType
    total_amount: Optional[float] = None
    estimated_completion: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
