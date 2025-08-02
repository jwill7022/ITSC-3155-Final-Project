from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import customers as model
from sqlalchemy.exc import SQLAlchemyError
from .base_controller import BaseCRUDController, handle_db_errors


class CustomerController(BaseCRUDController):
    def __init__(self):
        super().__init__(model.Customer)

    @handle_db_errors
    def create(self, db: Session, request) -> model.Customer:
        """Create a new customer, with validation for duplicate email."""
        existing_customer = db.query(model.Customer).filter(
            model.Customer.customer_email == request.customer_email
        ).first()
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer with email '{request.customer_email}' already exists"
            )

        return super().create(db, request)


# Create an instance of the controller
customer_controller = CustomerController()


def create(db: Session, request):
    return customer_controller.create(db, request)


def read_all(db: Session):
    return customer_controller.read_all(db)


def read_one(db: Session, item_id):
    return customer_controller.read_one(db, item_id)


def update(db: Session, item_id, request):
    return customer_controller.update(db, item_id, request)


def delete(db: Session, item_id):
    return customer_controller.delete(db, item_id)

