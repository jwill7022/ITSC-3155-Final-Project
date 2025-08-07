from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
import re


class CustomerBase(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100, description="Customer full name")
    customer_email: Optional[EmailStr] = Field(None, description="Valid email address")
    customer_phone: str = Field(..., description="Phone number")
    customer_address: Optional[str] = Field(None, max_length=200, description="Customer address")

    @field_validator('customer_phone')
    def validate_phone(cls, v):
        # Remove all non-digit characters
        phone_digits = re.sub(r'\D', '', v)

        # Check if it's a valid US phone number (10 digits)
        if len(phone_digits) == 10:
            return phone_digits
        elif len(phone_digits) == 11 and phone_digits.startswith('1'):
            return phone_digits[1:]  # Remove country code
        else:
            raise ValueError('Phone number must be 10 digits')

    @field_validator('customer_name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        # Remove extra spaces
        return ' '.join(v.split())


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=2, max_length=100)
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = Field(None, max_length=200)

    @field_validator('customer_phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        return CustomerBase.validate_phone(v)


class Customer(CustomerBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True