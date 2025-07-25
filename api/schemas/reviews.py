from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ReviewsBase(BaseModel):
    customer_name: str
    rating: int
    review_text: Optional[str] = None


class ReviewsCreate(ReviewsBase):
    pass


class Reviews(ReviewsBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True