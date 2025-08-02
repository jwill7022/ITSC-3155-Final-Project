from pydantic import BaseModel
from typing import List, Optional
from .orders import OrderType

class GuestOrderRequest(BaseModel):
    guest_name: str
    guest_phone: str
    guest_email: Optional[str] = None
    order_type: OrderType = OrderType.DINE_IN
    promotion_code: Optional[str] = None
    description: Optional[str] = None

class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int

class GuestOrderResponse(BaseModel):
    order_id: int
    tracking_number: str
    message: str
    estimated_completion: str
    total_amount: Optional[float] = None

class MenuSearchResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    calories: int
    food_category: str
    average_rating: Optional[float]
    review_count: int