from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import menu_item_ingredients as model
from ..schemas import menu_item_ingredients as schema
from .base_controller import BaseCRUDController
from ..utils.caching import cache
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any


class MenuItemIngredientController(BaseCRUDController[model.MenuItemIngredient, schema.MenuItemIngredientCreate, schema.MenuItemIngredientUpdate]):
    def __init__(self):
        super().__init__(model.MenuItemIngredient)

    def create(self, db: Session, request: schema.MenuItemIngredientCreate) -> model.MenuItemIngredient:
        """Override create to check for duplicate ingredient assignments and invalidate cache"""
        try:
            # Check for duplicate menu item ingredient assignment
            existing_item = db.query(self.model).filter(
                self.model.menu_item_id == request.menu_item_id,
                self.model.resource_id == request.resource_id
            ).first()
            if existing_item:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Menu item already has this ingredient assigned"
                )

            # Create the item using parent method
            new_item = super().create(db, request)

            # Invalidate menu cache
            self._invalidate_menu_cache()

            return new_item
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create menu item ingredient: {str(e)}"
            )

    def update(self, db: Session, item_id: int, request: schema.MenuItemIngredientUpdate) -> model.MenuItemIngredient:
        """Override update to invalidate cache"""
        updated_item = super().update(db, item_id, request)
        self._invalidate_menu_cache()
        return updated_item

    def get_ingredients_for_menu_item(self, db: Session, menu_item_id: int) -> List[Dict[str, Any]]:
        """Get all ingredients for a specific menu item"""
        try:
            ingredients = db.query(self.model).filter(
                self.model.menu_item_id == menu_item_id
            ).all()

            return [
                {
                    "ingredient_id": ingredient.id,
                    "resource_id": ingredient.resource_id,
                    "resource_name": ingredient.resource.item,
                    "amount": ingredient.amount
                }
                for ingredient in ingredients
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get ingredients: {str(e)}"
            )

    def _invalidate_menu_cache(self):
        """Invalidate menu-related cache entries"""
        cache.clear_pattern("menu_search:*")
        cache.clear_pattern("menu_item:*")


# Create controller instance
menu_item_ingredient_controller = MenuItemIngredientController()


# Function-based interface for backward compatibility
def create(db: Session, request: schema.MenuItemIngredientCreate):
    return menu_item_ingredient_controller.create(db, request)


def read_all(db: Session):
    return menu_item_ingredient_controller.read_all(db)


def read_one(db: Session, item_id: int):
    return menu_item_ingredient_controller.read_one(db, item_id)


def update(db: Session, item_id: int, request: schema.MenuItemIngredientUpdate):
    return menu_item_ingredient_controller.update(db, item_id, request)


def delete(db: Session, item_id: int):
    return menu_item_ingredient_controller.delete(db, item_id)


def get_ingredients_for_menu_item(db: Session, menu_item_id: int):
    return menu_item_ingredient_controller.get_ingredients_for_menu_item(db, menu_item_id)