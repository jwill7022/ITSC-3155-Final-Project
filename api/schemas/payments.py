from datetime import datetime
from pydantic import BaseModel


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_type: str  # "credit_card", "debit_card", "cash"
    status: str        # "completed", "pending", "failed"


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True