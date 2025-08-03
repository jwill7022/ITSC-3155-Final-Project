from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import menu_items as model
from ..schemas import menu_items as schema
from .base_controller import BaseCRUDController
from ..utils.caching import cache
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any


class MenuItemController(BaseCRUDController[model.MenuItem, schema.MenuItemsCreate, schema.MenuItemsUpdate]):
    def __init__(self):
        super().__init__(model.MenuItem)

    def create(self, db: Session, request: schema.MenuItemsCreate) -> model.MenuItem:
        """Override create to check for duplicate names and invalidate cache"""
        try:
            # Check for duplicate menu item name
            existing_item = db.query(self.model).filter(self.model.name == request.name).first()
            if existing_item:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Menu item with name '{request.name}' already exists"
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
                detail=f"Failed to create menu item: {str(e)}"
            )

    def update(self, db: Session, item_id: int, request: schema.MenuItemsUpdate) -> model.MenuItem:
        """Override update to invalidate cache"""
        updated_item = super().update(db, item_id, request)
        self._invalidate_menu_cache()
        return updated_item

    def update_availability(self, db: Session, item_id: int, available: bool) -> model.MenuItem:
        """Update only the availability status of a menu item"""
        try:
            item = db.query(self.model).filter(self.model.id == item_id).first()
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Menu item with id {item_id} not found"
                )

            item.is_available = available
            db.commit()
            db.refresh(item)

            # Invalidate cache
            self._invalidate_menu_cache()

            return item
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to update availability: {str(e)}"
            )

    def get_nutrition_info(self, db: Session, item_id: int) -> Dict[str, Any]:
        """Get nutrition and ingredient information for a menu item"""
        try:
            item = self.read_one(db, item_id)

            # Get ingredients
            ingredients = []
            for ingredient in item.menu_item_ingredients:
                ingredients.append({
                    "resource_name": ingredient.resource.item,
                    "amount": ingredient.amount,
                    "resource_id": ingredient.resource_id
                })

            return {
                "menu_item_id": item.id,
                "name": item.name,
                "calories": item.calories,
                "food_category": item.food_category.value,
                "ingredients": ingredients,
                "allergen_info": self._get_allergen_info(ingredients)
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get nutrition info: {str(e)}"
            )

    def _get_allergen_info(self, ingredients: List[Dict]) -> List[str]:
        """Determine potential allergens based on ingredients"""
        allergens = []
        allergen_keywords = {
            "dairy": ["milk", "cheese", "butter", "cream"],
            "gluten": ["wheat", "flour", "bread"],
            "nuts": ["peanut", "almond", "walnut", "cashew"],
            "soy": ["soy", "tofu"]
        }

        ingredient_names = [ing["resource_name"].lower() for ing in ingredients]

        for allergen, keywords in allergen_keywords.items():
            if any(keyword in " ".join(ingredient_names) for keyword in keywords):
                allergens.append(allergen)

        return allergens

    def _invalidate_menu_cache(self):
        """Invalidate menu-related cache entries"""
        cache.clear_pattern("menu_search:*")
        cache.clear_pattern("menu_item:*")


# Create controller instance
menu_item_controller = MenuItemController()


# Function-based interface for backward compatibility
def create(db: Session, request: schema.MenuItemsCreate):
    return menu_item_controller.create(db, request)


def read_all(db: Session, skip: int = 0, limit: int = 100, available_only: bool = True):
    if available_only:
        return db.query(model.MenuItem).filter(model.MenuItem.is_available == True).offset(skip).limit(limit).all()
    return menu_item_controller.read_all(db, skip, limit)


def read_one(db: Session, item_id: int):
    return menu_item_controller.read_one(db, item_id)


def update(db: Session, item_id: int, request: schema.MenuItemsUpdate):
    return menu_item_controller.update(db, item_id, request)


def update_availability(db: Session, item_id: int, available: bool):
    return menu_item_controller.update_availability(db, item_id, available)


def get_nutrition_info(db: Session, item_id: int):
    return menu_item_controller.get_nutrition_info(db, item_id)


def delete(db: Session, item_id: int):
    return menu_item_controller.delete(db, item_id)