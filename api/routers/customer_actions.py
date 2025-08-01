from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..services.order_services import OrderService
from ..services.menu_services import MenuService
from ..models.menu_items import FoodCategory
from ..schemas.orders import GuestOrderCreate, OrderTrack
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Customer Actions'],
    prefix="/customer_actions",
)

@router.post("/orders/guest", response_model=dict)
def place_guest_order(
    request: GuestOrderCreate,
    order_items: List[dict],  # [{"menu_item_id": 1, "quantity": 2}]
    db: Session = Depends(get_db)
):
    """Place order as guest customer"""
    guest_info = {
        "guest_name": request.guest_name,
        "guest_phone": request.guest_phone,
        "guest_email": request.guest_email,
        "description": request.description,
        "order_type": request.order_type,
        "promotion_code": request.promotion_code
    }

    order = OrderService.create_order(db=db, order_items=order_items)

    return{
        "order_id": order.id,
        "tracking_number": order.tracking_number,
        "message": "Order placed successfully! Save your tracking number.",
        "estimated_completion": "30-45 minutes",
        "total_amount": float(order.total_amount) if order.total_amount else None
    }

@router.get("/orders/track/{tracking_number}", response_model=OrderTrack)
def track_my_order(tracking_number: str, db: Session = Depends(get_db)):
    """Track order status by tracking number"""
    return OrderService.track_order(db, tracking_number)

@router.get("/menu/search")
def search_menu(
        search_term: Optional[str] = Query(None, description="Search for dishes"),
        category: Optional[FoodCategory] = Query(None, description="vegetarian, vegan, gluten_free, regular"),
        max_price: Optional[float] = Query(None, description="Maximum price"),
        sort_by: str = Query("name", description="Sort by: name, price_asc, price_desc"),
        db: Session = Depends(get_db)
):
    """Search menu for specific dietary preferences"""
    return MenuService.search_menu_items(
        db, search_term=search_term, category=category,
        max_price=max_price, sort_by=sort_by
    )

@router.post("/orders/{order_id}/apply-promotion")
def apply_promotion_code(
        order_id: str,
        promotion_code: str,
        db: Session = Depends(get_db)
):
    """Apply promotion code to order"""
    #Skeleton function for now, needs implementation.
    #Implementation would recalculate order total with discount
    return {"message": "Promotion code applied", "order_id": order_id}