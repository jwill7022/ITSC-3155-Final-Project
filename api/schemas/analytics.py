from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MenuPerformance(BaseModel):
    menu_item_id: int
    name: str
    price: float
    order_count: int
    total_quantity_sold: int
    total_revenue: float
    average_rating: Optional[float]
    review_count: int
    popularity_score: float
    performance_status: str

class ReviewInsight(BaseModel):
    customer_name: str
    rating: int
    review_text: str
    created_at: datetime
    menu_item_id: int

class ReviewAnalytics(BaseModel):
    total_reviews: int
    average_rating: float
    rating_distribution: dict
    recent_complaints: List[ReviewInsight]
    satisfaction_summary: str
    recommendations: List[str]

class RevenueReport(BaseModel):
    date: str
    total_revenue: float
    order_count: int