from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from ..services import staff_services
from ..services.order_services import OrderService
from ..services.inventory_services import InventoryService
from ..services.analytics_services import AnalyticsService
from ..schemas import menu_items as schema
from ..schemas import promotions as promotion_schema
from ..dependencies.database import get_db

# holds common actions made by the staff

router = APIRouter(
    tags=['Staff Actions'],
    prefix="/staff_actions",
)


# Existing ingredient checking
@router.get("/")
def view_ingredients(menu_item_id: int, quantity: int, db: Session = Depends(get_db)):
    return staff_services.get_required_ingredients(db, menu_item_id, quantity)


# Inventory Management
@router.get("/inventory/low-stock")
def get_low_stock_items(
        threshold: int = Query(10, description="Stock threshold"),
        db: Session = Depends(get_db)
):
    """Get items with low stock"""
    return InventoryService.get_low_stock_items(db, threshold)


@router.post("/inventory/check-availability")
def check_inventory_availability(
        order_items: list[dict],  # [{"menu_item_id": 1, "quantity": 2}]
        db: Session = Depends(get_db)
):
    """Check if order items can be fulfilled"""
    return InventoryService.check_availability(db=db, order_items=order_items)


# Order Management - FIXED
@router.get("/orders/date-range")
def get_orders_by_date_range(
        start_date: date = Query(..., description="Start date (YYYY-MM-DD)", example="2024-01-01"),
        end_date: date = Query(..., description="End date (YYYY-MM-DD)", example="2024-01-31"),
        db: Session = Depends(get_db)
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


# Revenue Reporting - FIXED
@router.get("/revenue/daily")
def get_daily_revenue(
        target_date: date = Query(..., description="Date for revenue calculation (YYYY-MM-DD)", example="2024-01-15"),
        db: Session = Depends(get_db)
):
    """Calculate total revenue for a specific date - FIXED"""
    return OrderService.calculate_daily_revenue(db, target_date)


@router.get("/analytics/menu-performance")
def get_menu_performance(db: Session = Depends(get_db)):
    """Get menu performance analytics"""
    return AnalyticsService.get_menu_item_performance(db)


@router.get("/analytics/review-insights")
def get_review_insights(
        menu_item_id: Optional[int] = Query(None, description="Filter by menu item"),
        db: Session = Depends(get_db)
):
    """Get review insights and sentiment analysis"""
    return AnalyticsService.get_review_insights(db, menu_item_id)


# Promotion management
@router.get("/promotions/code/{promo_code}", response_model=promotion_schema.Promotion)
def get_promotion_by_code(promo_code: str, db: Session = Depends(get_db)):
    return staff_services.get_promotion_by_code(db, promo_code=promo_code)


@router.put("/promotions/code/{promo_code}", response_model=promotion_schema.Promotion)
def update_promotion_by_code(promo_code: str, request: promotion_schema.PromotionUpdate, db: Session = Depends(get_db)):
    return staff_services.update_promotion_by_code(db=db, promo_code=promo_code, request=request)


@router.delete("/promotions/code/{promo_code}")
def delete_promotion_by_code(promo_code: str, db: Session = Depends(get_db)):
    return staff_services.delete_promotion_by_code(db=db, promo_code=promo_code)