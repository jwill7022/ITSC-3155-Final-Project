from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import reviews as model
from ..models.menu_items import MenuItem
from sqlalchemy.exc import SQLAlchemyError
from .base_controller import BaseCRUDController, handle_db_errors


class ReviewController(BaseCRUDController):
    def __init__(self):
        super().__init__(model.Reviews)

    @handle_db_errors
    def create(self, db: Session, request):
        # Validate that menu item exists
        menu_item = db.query(MenuItem).filter(MenuItem.id == request.menu_item_id).first()
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with id {request.menu_item_id} not found"
            )

        return super().create(db, request)


# Create controller instance
review_controller = ReviewController()

def create(db: Session, request):
    return review_controller.create(db, request)

def read_all(db: Session):
    return review_controller.read_all(db)

def read_one(db: Session, item_id):
    return review_controller.read_one(db, item_id)

def update(db: Session, item_id, request):
    return review_controller.update(db, item_id, request)

def delete(db: Session, item_id):
    return review_controller.delete(db, item_id)

