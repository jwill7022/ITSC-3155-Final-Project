from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, and_
from datetime import datetime, date
from typing import List, Dict, Optional
from ..models.orders import Order
from ..models.order_details import OrderDetail
from ..models.menu_items import MenuItem
from ..models.promotions import Promotion
from .inventory_services import InventoryService
import decimal

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
            #Check inventory before anything else
            inventory_check = InventoryService.check_inventory(db, order_items)
            if not inventory_check["all_available"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient inventory for items: {inventory_check['insufficient_items']}"
                )

            #Create order
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
            db.flush() #Retrieve ID without committing

            #Add order details
            total_amount = 0
            for item in order_items:
                menu_item = db.query(MenuItem).filter(MenuItem.id == item["menu_item_id"]).first()
                if not menu_item:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Menu item  {item['menu_item_id']} not found"
                    )

                order_detail = OrderDetail(
                    order_id=new_order.id,
                    menu_item_id=item["menu_item_id"],
                    amount=item["quantity"]
                )
                db.add(order_detail)
                total_amount += float(menu_item.price) * item["quantity"]

            #Calculate totals
            subtotal = decimal.Decimal(str(total_amount))
            discount = OrderService._calculate_discount(db, new_order.promotion_code, subtotal)
            tax_rate = decimal.Decimal("0.07") #NC 7% sales tax

            new_order.subtotal = subtotal
            new_order.discount_amount = discount
            new_order.tax_amount = (subtotal - discount) * tax_rate
            new_order.total_amount = subtotal - discount + new_order.tax_amount

            db.commit()
            db.refresh(new_order)
            return new_order

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create order: {str(e)}"
            )

    @staticmethod
    def _calculate_discount(db: Session, promo_code: Optional[str], subtotal: decimal.Decimal) -> decimal.Decimal:
        """Calculate discount amount from promo code"""
        if not promo_code:
            return decimal.Decimal("0")

        promotion = db.query(Promotion).filter(Promotion.code == promo_code).first()
        if not promotion:
            return decimal.Decimal("0")

        #Check if expired
        if promotion.expiration_date and promotion.expiration_date < datetime.now():
            return decimal.Decimal("0")

        discount_percent = decimal.Decimal(str(promotion.discount_percent)) / 100
        return subtotal * discount_percent

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

            #Calculate estimated completion time based on order status
            estimated_completion = None
            if order.status.value in ["pending", "confirmed", "in_progress"]:
                #Add 30-45 minutes based on order type
                minutes_to_add = 30 if order.order_type.value == "dine_in" else 45
                estimated_completion = order.order_date.replace(
                    minute=order.order_date.minute + minutes_to_add
                )

            return {
                "id": order.id,
                "tracking_number": order.tracking_number,
                "status": order.status.value,
                "order_date": order.order_date,
                "order_type": order.order_type.value,
                "total_amount": float(order.total_amount) if order.total_amount else None,
                "estimated_completion": estimated_completion,
                "customer_name": order.guest_name or (order.customer_name if order.customer else None)
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )

    @staticmethod
    def get_orders_by_date_range(db: Session, start_date: date, end_date: date) -> List[Dict]:
        """Get orders within date range"""
        try:
            orders = db.query(Order).filter(
                and_(
                    func.date(Order.order_date) >= start_date,
                    func.date(Order.order_date) <= end_date
                     )
            ).all()

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

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )

    @staticmethod
    def calculate_daily_revenue(db: Session, target_date: date) -> Dict:
        """Calculate total revenue for a specific date"""
        try:
            result = db.query(
                func.sum(Order.total_amount).label("total_revenue"),
                func.count(Order.id).label("order_count")
            ).filter(
                and_(
                    func.date(Order.order_date) == target_date,
                    Order.status != "cancelled"
                )
            ).first()

            return {
                "date": target_date.isoformat(),
                "total_revenue": float(result.total_revenue) if result.total_revenue else 0,
                "order_count": result.order_count
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )