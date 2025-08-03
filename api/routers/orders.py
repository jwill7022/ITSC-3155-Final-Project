from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..services.order_services import OrderService
from ..services.inventory_services import InventoryService
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.post("/guest", response_model=schema.Order)
def create_guest_order(
        request: schema.GuestOrderCreate,
        order_items: List[dict],  # [{"menu_item_id": 1, "quantity": 2}]
        db: Session = Depends(get_db)
):
    """Create order for guest customer without account"""
    guest_info = {
        "guest_name": request.guest_name,
        "guest_phone": request.guest_phone,
        "guest_email": request.guest_email,
        "description": request.description,
        "order_type": request.order_type,
        "promotion_code": request.promotion_code
    }
    return controller.create_guest_order(db, guest_info, order_items)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/track/{tracking_number}", response_model=schema.OrderTrack)
def track_order(tracking_number: str, db: Session = Depends(get_db)):
    """Track order by tracking number"""
    return controller.track_order(db, tracking_number)


@router.get("/date-range")
def get_orders_by_date_range(
        start_date: date = Query(..., description="Start date (YYYY-MM-DD)", example="2024-01-01"),
        end_date: date = Query(..., description="End date (YYYY-MM-DD)", example="2024-01-31"),
        db: Session = Depends(get_db),
):
    """Get orders within date range - FIXED with proper validation"""
    # Validate date range
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before or equal to end date"
        )

    # Check if date range is not too large (optional safety measure)
    if (end_date - start_date).days > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date range cannot exceed 365 days"
        )

    return OrderService.get_orders_by_date_range(db, start_date, end_date)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.put("/{order_id}/confirm", response_model=schema.Order)
def confirm_order(order_id: int, db: Session = Depends(get_db)):
    """Confirm order and deduct inventory"""
    return controller.confirm_order(db, order_id)


@router.post("/{order_id}/check-inventory")
def check_order_inventory(order_id: int, db: Session = Depends(get_db)):
    """Check if order can be fulfilled with current inventory"""
    order = controller.read_one(db, order_id)
    order_items = [
        {"menu_item_id": detail.menu_item_id, "quantity": detail.amount}
        for detail in order.order_details
    ]
    return InventoryService.check_availability(db, order_items)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)