from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from .payments import Payment



class OrderBase(BaseModel):
    customer_id: int
    description: Optional[str] = None
    status: Optional[str] = "pending"


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None
    payments: Optional[Payment] = None

    class ConfigDict:
        from_attributes = True
