from typing import Optional
from pydantic import BaseModel
from enum import Enum

class FoodCategory(str, Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    REGULAR = "regular"


class MenuItemsBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    calories: int
    food_category: FoodCategory

class MenuItemsCreate(MenuItemsBase):
    pass

class MenuItemsUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    food_category: Optional[FoodCategory] = None

class MenuItems(MenuItemsBase):
    id: int

    class ConfigDict:
        from_attributes = True