from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import menu_item_ingredients as model
from ..models.menu_items import MenuItem
from ..models.resources import Resource
from sqlalchemy.exc import SQLAlchemyError
from .base_controller import BaseCRUDController, handle_db_errors


class MenuItemIngredientController(BaseCRUDController):
    def __init__(self):
        super().__init__(model.MenuItemIngredient)

    @handle_db_errors
    def create(self, db: Session, request):
        # Validate that menu item exists
        menu_item = db.query(MenuItem).filter(MenuItem.id == request.menu_item_id).first()
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with id {request.menu_item_id} not found"
            )

        # Validate that resource exists
        resource = db.query(Resource).filter(Resource.id == request.resource_id).first()
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource with id {request.resource_id} not found"
            )

        # Check for duplicate ingredient
        existing = db.query(model.MenuItemIngredient).filter(
            model.MenuItemIngredient.menu_item_id == request.menu_item_id,
            model.MenuItemIngredient.resource_id == request.resource_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ingredient {resource.item} already exists for menu item {menu_item.name}"
            )

        return super().create(db, request)


# Create controller instance
menu_item_ingredient_controller = MenuItemIngredientController()


def create(db: Session, request):
    return menu_item_ingredient_controller.create(db, request)


def read_all(db: Session):
    return menu_item_ingredient_controller.read_all(db)


def read_one(db: Session, item_id):
    return menu_item_ingredient_controller.read_one(db, item_id)


def update(db: Session, item_id, request):
    return menu_item_ingredient_controller.update(db, item_id, request)


def delete(db: Session, item_id):
    return menu_item_ingredient_controller.delete(db, item_id)

