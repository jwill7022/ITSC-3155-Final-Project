from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import menu_items as model
from sqlalchemy.exc import SQLAlchemyError
from .base_controller import BaseCRUDController, handle_db_errors


class MenuItemController(BaseCRUDController):
    def __init__(self):
        super().__init__(model.MenuItem)

    @handle_db_errors
    def create(self, db: Session, request) -> model.MenuItem:
        """Create a new menu item, with validation for duplicate name."""
        existing_item = db.query(model.MenuItem).filter(
            model.MenuItem.name == request.name
        ).first()
        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item with name '{request.name}' already exists"
            )

        return super().create(db, request)

    @handle_db_errors
    def update_availability(self, db: Session, item_id: int, is_available: bool) -> model.MenuItem:
        """Update the availability status of a menu item."""
        menu_item = self.read_one(db, item_id)
        menu_item.is_available = is_available
        db.commit()
        db.refresh(menu_item)
        return menu_item


# Create controller instance
menu_item_controller = MenuItemController()

def create(db: Session, request):
    return menu_item_controller.create(db, request)

def read_all(db: Session):
    return menu_item_controller.read_all(db)

def read_one(db: Session, item_id):
    return menu_item_controller.read_one(db, item_id)

def update(db: Session, item_id, request):
    return menu_item_controller.update(db, item_id, request)

def delete(db: Session, item_id):
    return menu_item_controller.delete(db, item_id)

def update_availability(db: Session, item_id: int, is_available: bool):
    return menu_item_controller.update_availability(db, item_id, is_available)
