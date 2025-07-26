from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ReviewsBase(BaseModel):
    menu_item_id: int
    customer_name: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    review_text: Optional[str] = None


class ReviewsCreate(ReviewsBase):
    pass


class Reviews(ReviewsBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True