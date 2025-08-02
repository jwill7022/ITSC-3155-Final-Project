from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import resources as model
from sqlalchemy.exc import SQLAlchemyError
from .base_controller import BaseCRUDController, handle_db_errors


class ResourceController(BaseCRUDController):
    def __init__(self):
        super().__init__(model.Resource)

    @handle_db_errors
    def create(self, db: Session, request) -> model.Resource:
        """Create a new resource, with validation for duplicate item name."""
        existing_resource = db.query(model.Resource).filter(
            model.Resource.item == request.item
        ).first()
        if existing_resource:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Resource '{request.item}' already exists"
            )

        return super().create(db, request)

    @handle_db_errors
    def update_availability(self, db: Session, item_id: int, new_amount: int) -> model.Resource:
        """
        Update the availability of a resource item.
        This function is intended for cases where we only want to update the amount of an existing resource,
        for example, when receiving new stock or deducting inventory for an order.
        """
        if new_amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New amount cannot be negative."
            )

        resource = self.read_one(db, item_id)
        resource.amount = new_amount
        db.commit()
        db.refresh(resource)
        return resource


# Create controller instance
resource_controller = ResourceController()


def create(db: Session, request):
    return resource_controller.create(db, request)


def read_all(db: Session):
    return resource_controller.read_all(db)


def read_one(db: Session, item_id):
    return resource_controller.read_one(db, item_id)


def update(db: Session, item_id, request):
    return resource_controller.update(db, item_id, request)


def delete(db: Session, item_id):
    return resource_controller.delete(db, item_id)


def update_availability(db: Session, item_id: int, new_amount: int):
    return resource_controller.update_availability(db, item_id, new_amount)
