from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional

class PaymentType(str, Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_type: PaymentType = None
    status: PaymentStatus = PaymentStatus.PENDING


class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_type: Optional[PaymentType] = None
    status: Optional[PaymentStatus] = None


class Payment(PaymentBase):
    id: int
    payment_date: datetime

    class ConfigDict:
        from_attributes = True