from sqlalchemy import Column, Integer, String, Numeric, Enum, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
import enum

class FoodCategory(enum.Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    REGULAR = "regular"
    KETO = "keto"
    LOW_CARB = "low_carb"

class MenuItem(Base):
    __tablename__ = "menu_items"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String(255), unique=True, nullable=False, index=True)
    description   = Column(String(255), nullable=True)
    price         = Column(Numeric(10, 2), nullable=False)
    calories      = Column(Integer, nullable=False)
    food_category = Column(Enum(FoodCategory), nullable=False, index=True, default=FoodCategory.REGULAR)
    is_available = Column(Boolean, nullable=False, default=True, index=True)

    menu_item_ingredients = relationship(
        "MenuItemIngredient",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )
    order_details = relationship(
        "OrderDetail",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Reviews",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )