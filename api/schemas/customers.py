from pydantic import BaseModel
from typing import Optional


class CustomerBase(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: int
    customer_address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class ConfigDict:
        from_attributes = True