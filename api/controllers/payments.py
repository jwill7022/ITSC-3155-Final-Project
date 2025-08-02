from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import payments as model
from ..models.orders import Order
from sqlalchemy.exc import SQLAlchemyError
from .base_controller import BaseCRUDController, handle_db_errors


class PaymentController(BaseCRUDController):
    def __init__(self):
        super().__init__(model.Payment)

    @handle_db_errors
    def create(self, db: Session, request):
        # First check if the order exists
        order = db.query(Order).filter(Order.id == request.order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {request.order_id} not found"
            )

        return super().create(db, request)

    @handle_db_errors
    def update(self, db: Session, item_id, request):
        # Validate order exists if order_id is being updated
        if hasattr(request, 'order_id') and request.order_id:
            order = db.query(Order).filter(Order.id == request.order_id).first()
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Order with id {request.order_id} not found"
                )

        return super().update(db, item_id, request)


# Create controller instance
payment_controller = PaymentController()


def create(db: Session, request):
    return payment_controller.create(db, request)


def read_all(db: Session):
    return payment_controller.read_all(db)


def read_one(db: Session, item_id):
    return payment_controller.read_one(db, item_id)


def update(db: Session, item_id, request):
    return payment_controller.update(db, item_id, request)


def delete(db: Session, item_id):
    return payment_controller.delete(db, item_id)

