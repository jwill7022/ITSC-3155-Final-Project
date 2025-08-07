from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import orders as model
from ..schemas import orders as schema
from ..services.order_services import OrderService
from ..services.inventory_services import InventoryService
from .base_controller import BaseCRUDController
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict

class OrderController(BaseCRUDController[model.Order, schema.OrderCreate, schema.OrderUpdate]):
    def __init__(self):
        super().__init__(model.Order)

    def create_guest_order(self, db: Session, guest_info: Dict, order_items: List[Dict]):
        """Create order for guest customer"""
        return OrderService.create_guest_order(db, guest_info, order_items)

    def track_order(self, db: Session, tracking_number: str):
        """Track order by tracking number"""
        return OrderService.track_order(db, tracking_number)

    def confirm_order(self, db: Session, order_id: int):
        """Confirm order and deduct inventory"""
        try:
            order = self.read_one(db, order_id)

            # Get order items for inventory deduction
            order_items = [
                {"menu_item_id": detail.menu_item_id, "quantity": detail.amount}
                for detail in order.order_details
            ]

            # Deduct inventory
            InventoryService.deduct_inventory(db, order_items)

            # Update order status
            order.status = model.StatusType.CONFIRMED
            db.commit()
            db.refresh(order)

            return order

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to confirm order: {str(e)}"
            )

# Create controller instance
order_controller = OrderController()

# Function-based interface
def create(db: Session, request: schema.OrderCreate):
    return order_controller.create(db, request)

def create_guest_order(db: Session, guest_info: Dict, order_items: List[Dict]):
    return order_controller.create_guest_order(db, guest_info, order_items)

def read_all(db: Session):
    return order_controller.read_all(db)

def read_one(db: Session, item_id: int):
    return order_controller.read_one(db, item_id)

def update(db: Session, item_id: int, request: schema.OrderUpdate):
    return order_controller.update(db, item_id, request)

def delete(db: Session, item_id: int):
    return order_controller.delete(db, item_id)

def track_order(db: Session, tracking_number: str):
    return order_controller.track_order(db, tracking_number)

def confirm_order(db: Session, order_id: int):
    return order_controller.confirm_order(db, order_id)