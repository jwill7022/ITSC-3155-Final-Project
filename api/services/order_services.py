from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, and_
from datetime import datetime, date, timedelta, time
from typing import List, Dict, Optional
from ..models.orders import Order, StatusType
from ..models.order_details import OrderDetail
from ..models.menu_items import MenuItem
from ..models.promotions import Promotion
from .inventory_services import InventoryService
from decimal import Decimal
import logging

# logging setup
logger = logging.getLogger(__name__)


class OrderService:

    @staticmethod
    def create_guest_order(db: Session, guest_info: Dict, order_items: List[Dict]) -> Order:
        """
        Create order for guest customer
        :param db:
        :param guest_info:
        :param order_items:
        :return:
        """

        try:
            # Validate order items first
            if not order_items:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Order must contain at least one item"
                )
            # Check inventory availability
            inventory_check = InventoryService.check_availability(db, order_items)
            if not inventory_check["all_available"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Insufficient inventory",
                        "unavailable_items": inventory_check["insufficient_items"],
                        "details": inventory_check["details"]
                    }
                )

            # Validate menu items exist and are available
            menu_item_ids = [item["menu_item_id"] for item in order_items]
            menu_items = db.query(MenuItem).filter(
                MenuItem.id.in_(menu_item_ids),
                MenuItem.is_available == True
            ).all()

            if len(menu_items) != len(menu_item_ids):
                unavailable_ids = set(menu_item_ids) - {item.id for item in menu_items}
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Menu items not available: {list(unavailable_ids)}"
                )

            # Create order
            new_order = Order(
                customer_id=None,
                guest_name=guest_info["guest_name"],
                guest_phone=guest_info["guest_phone"],
                guest_email=guest_info.get("guest_email"),
                description=guest_info.get("description"),
                order_type=guest_info.get("order_type", "dine_in"),
                promotion_code=guest_info.get("promotion_code")
            )

            db.add(new_order)
            db.flush()  # Retrieve ID without committing

            # Add order details and calculate total
            total_amount = Decimal("0")
            menu_items_dict = {item.id: item for item in menu_items}

            for item in order_items:
                menu_item_id = item["menu_item_id"]
                quantity = item["quantity"]

                if quantity <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid quantity: {quantity} for menu item {menu_item_id}"
                    )

                menu_item = menu_items_dict[menu_item_id]

                order_detail = OrderDetail(
                    order_id=new_order.id,
                    menu_item_id=menu_item_id,
                    amount=quantity
                )
                db.add(order_detail)

                item_total = Decimal(str(menu_item.price)) * quantity
                total_amount += item_total

            # Calculate discounts and taxes
            subtotal = total_amount
            discount = OrderService._calculate_discount(db, new_order.promotion_code, subtotal)
            tax_rate = Decimal("0.07")  # NC 7% sales tax
            tax_amount = (subtotal - discount) * tax_rate

            new_order.subtotal = subtotal
            new_order.discount_amount = discount
            new_order.tax_amount = tax_amount
            new_order.total_amount = subtotal - discount + tax_amount

            # Set estimated completion time
            new_order.estimated_completion = OrderService._calculate_estimated_completion(
                new_order.order_type, len(order_items)
            )

            db.commit()
            db.refresh(new_order)
            return new_order

        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create guest order: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create order"
            )

    @staticmethod
    def _calculate_estimated_completion(order_type: str, item_count: int) -> datetime:
        """Calculate estimated completion time based on order type and complexity"""
        base_minutes = 20

        if order_type == "delivery":
            base_minutes += 30
        elif order_type == "takeout":
            base_minutes += 10

        # Add time based on number of items
        additional_minutes = min(item_count * 2, 20)

        return datetime.now() + timedelta(minutes=base_minutes + additional_minutes)

    @staticmethod
    def _calculate_discount(db: Session, promo_code: Optional[str], subtotal: Decimal) -> Decimal:
        """Calculate discount amount from promo code with validation"""
        if not promo_code:
            return Decimal("0")

        promotion = db.query(Promotion).filter(Promotion.code == promo_code).first()
        if not promotion:
            logger.warning(f"Invalid promo code used: {promo_code}")
            return Decimal("0")

        # Check expiry status
        if promotion.expiration_date and promotion.expiration_date < datetime.now():
            logger.warning(f"Expired promo code used: {promo_code}")
            return Decimal("0")

        discount_percent = Decimal(str(promotion.discount_percent)) / 100
        discount_amount = subtotal * discount_percent

        # Log successful discount application
        logger.info(f"Applied discount: {promo_code}, amount: {discount_amount}")
        return discount_amount

    @staticmethod
    def track_order(db: Session, tracking_number: str) -> Dict:
        """Track order by tracking number"""
        try:
            order = db.query(Order).filter(Order.tracking_number == tracking_number).first()
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )

            # Get order items for display
            order_items = []
            for detail in order.order_details:
                order_items.append({
                    "name": detail.menu_item.name,
                    "quantity": detail.amount,
                    "price": float(detail.menu_item.price)
                })

            # Calculate remaining time
            estimated_completion = order.estimated_completion
            time_remaining = None
            if estimated_completion and order.status.value in ["pending", "confirmed", "in_progress"]:
                remaining_delta = estimated_completion - datetime.now()
                if remaining_delta.total_seconds() > 0:
                    time_remaining = int(remaining_delta.total_seconds() / 60)  # minutes instead of seconds

            return {
                "id": order.id,
                "tracking_number": order.tracking_number,
                "status": order.status.value,
                "order_date": order.order_date,
                "order_type": order.order_type.value,
                "total_amount": float(order.total_amount) if order.total_amount else None,
                "estimated_completion": estimated_completion,
                "time_remaining_minutes": time_remaining,
                "customer_name": order.guest_name or (order.customer.customer_name if order.customer else "Unknown"),
                "order_items": order_items,
                "status_history": OrderService._get_status_history(order)

            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to track order {tracking_number}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to track order"
            )

    @staticmethod
    def _get_status_history(order: Order) -> List[Dict]:
        """Get status history for order (Simple/Not reflecting actual implementation"""
        history = [
            {
                "status": "pending",
                "timestamp": order.order_date,
                "description": "Order received"
            }
        ]

        if order.status.value != "pending":
            history.append({
                "status": order.status.value,
                "timestamp": datetime.now(),
                "description": f"Order {order.status.value}"
            })

        return history

    @staticmethod
    def update_order_status(db: Session, order_id: int, new_status: StatusType) -> Order:
        """Update order status with validation"""
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )

            # Validate status transition
            valid_transitions = OrderService._get_valid_status_transitions()
            current_status = order.status.value

            if new_status.value not in valid_transitions.get(current_status, []):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot change status from {current_status} to {new_status.value}"
                )

            order.status = new_status
            db.commit()
            db.refresh(order)

            logger.info(f"Order {order_id} status updated to {new_status.value}")
            return order

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update order status: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update order status"
            )

    @staticmethod
    def _get_valid_status_transitions() -> Dict[str, List[str]]:
        """Define valid status transitions"""
        return {
            "pending": ["confirmed", "cancelled"],
            "confirmed": ["in_progress", "cancelled"],
            "in_progress": ["awaiting_pickup", "out_for_delivery", "completed"],
            "awaiting_pickup": ["completed", "cancelled"],
            "out_for_delivery": ["completed", "cancelled"],
            "cancelled": [],  # Terminal state
            "completed": []  # Terminal state
        }

    @staticmethod
    def get_orders_by_date_range(db: Session, start_date: date, end_date: date) -> List[Dict]:
        """Get orders within date range - FIXED VERSION"""
        try:
            # Convert dates to datetime objects to include full day range
            start_datetime = datetime.combine(start_date, time.min)  # 00:00:00
            end_datetime = datetime.combine(end_date, time.max)  # 23:59:59.999999

            # Validate date range
            if start_date > end_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start date must be before or equal to end date"
                )

            orders = db.query(Order).filter(
                and_(
                    Order.order_date >= start_datetime,
                    Order.order_date <= end_datetime
                )
            ).order_by(Order.order_date.desc()).all()

            return [
                {
                    "id": order.id,
                    "tracking_number": order.tracking_number,
                    "order_date": order.order_date,
                    "status": order.status.value,
                    "total_amount": float(order.total_amount) if order.total_amount else 0,
                    "customer_name": order.guest_name or (order.customer.customer_name if order.customer else "Unknown")
                }
                for order in orders
            ]

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )

    @staticmethod
    def calculate_daily_revenue(db: Session, target_date: date) -> Dict:
        """Calculate total revenue for a specific date - ONLY COMPLETED ORDERS"""
        try:
            start_of_day = datetime.combine(target_date, datetime.min.time())
            end_of_day = start_of_day + timedelta(days=1)

            result = db.query(
                func.sum(Order.total_amount).label("total_revenue"),
                func.count(Order.id).label("order_count")
            ).filter(
                and_(
                    Order.order_date >= start_of_day,
                    Order.order_date < end_of_day,
                    Order.status == StatusType.COMPLETED  #only completed orders
                )
            ).first()

            total_revenue = float(result.total_revenue) if result.total_revenue else 0.0
            order_count = result.order_count if result.order_count else 0

            return {
                "date": target_date.isoformat(),
                "total_revenue": total_revenue,
                "order_count": order_count
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )