from typing import Optional
from pydantic import BaseModel

class MenuItemsBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    calories: int
    food_category: str

class MenuItemsCreate(MenuItemsBase):
    pass

class MenuItemsUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    calories: int
    food_category: str

class MenuItems(MenuItemsBase):
    id: int

    class ConfigDict:
        from_attributes = True