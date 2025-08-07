from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum


class FoodCategory(str, Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    REGULAR = "regular"
    KETO = "keto"
    LOW_CARB = "low_carb"


class MenuItemsBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Menu item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Price in USD")
    calories: int = Field(..., ge=0, le=5000, description="Calories per serving")
    food_category: FoodCategory = Field(default=FoodCategory.REGULAR)
    is_available: bool = Field(default=True, description="Whether item is currently available")

    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    @field_validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return round(v, 2)

    @field_validator('food_category', mode='before')
    def validate_food_category(cls, v):
        """Convert string to enum if necessary"""
        if isinstance(v, str):
            # Handle case-insensitive conversion
            v_lower = v.lower()
            for category in FoodCategory:
                if category.value == v_lower:
                    return category
            # If not found, raise error with valid options
            valid_options = [cat.value for cat in FoodCategory]
            raise ValueError(f'Invalid food category. Must be one of: {valid_options}')
        return v


class MenuItemsCreate(MenuItemsBase):
    pass


class MenuItemsUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    calories: Optional[int] = Field(None, ge=0, le=5000)
    food_category: Optional[FoodCategory] = None
    is_available: Optional[bool] = None

    @field_validator('food_category', mode='before')
    def validate_food_category(cls, v):
        """Convert string to enum if necessary"""
        if v is None:
            return v
        if isinstance(v, str):
            v_lower = v.lower()
            for category in FoodCategory:
                if category.value == v_lower:
                    return category
            valid_options = [cat.value for cat in FoodCategory]
            raise ValueError(f'Invalid food category. Must be one of: {valid_options}')
        return v


class MenuItemsResponse(MenuItemsBase):
    id: int
    created_at: Optional[datetime] = None
    average_rating: Optional[float] = None
    review_count: int = 0

    class Config:
        from_attributes = True