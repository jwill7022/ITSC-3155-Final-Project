from pydantic import BaseModel
from typing import Optional


class CustomerBase(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: int
    customer_address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    customer_name = Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[int] = None
    customer_address: Optional[str] = None


class Customer(CustomerBase):
    id: int

    class ConfigDict:
        from_attributes = True