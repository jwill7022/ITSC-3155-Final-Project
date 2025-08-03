from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import order_details as model
from ..models.orders import Order
from ..models.menu_items import MenuItem
from sqlalchemy.exc import SQLAlchemyError
from .base_controller import BaseCRUDController, handle_db_errors


class OrderDetailController(BaseCRUDController):
    def __init__(self):
        super().__init__(model.OrderDetail)

    @handle_db_errors
    def create(self, db: Session, request):
        # Validate that order exists
        order = db.query(Order).filter(Order.id == request.order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {request.order_id} not found"
            )

        # Validate that menu item exists
        menu_item = db.query(MenuItem).filter(MenuItem.id == request.menu_item_id).first()
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with id {request.menu_item_id} not found"
            )

        # Check if this menu item already exists in the order
        existing_detail = db.query(model.OrderDetail).filter(
            model.OrderDetail.order_id == request.order_id,
            model.OrderDetail.menu_item_id == request.menu_item_id
        ).first()

        if existing_detail:
            # Update existing quantity instead of creating duplicate
            existing_detail.amount += request.amount
            try:
                db.commit()
                db.refresh(existing_detail)
            except SQLAlchemyError as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))
            return existing_detail

        return super().create(db, request)


# Create controller instance
order_detail_controller = OrderDetailController()


def create(db: Session, request):
    return order_detail_controller.create(db, request)


def read_all(db: Session):
    return order_detail_controller.read_all(db)


def read_one(db: Session, item_id):
    return order_detail_controller.read_one(db, item_id)


def update(db: Session, item_id, request):
    return order_detail_controller.update(db, item_id, request)


def delete(db: Session, item_id):
    return order_detail_controller.delete(db, item_id)

