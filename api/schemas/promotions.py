from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PromotionBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_percent: int
    expiration_date: Optional[str] = None


class PromotionCreate(PromotionBase):
    pass


class Promotion(PromotionBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True