from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItems(Base):
    __tablename__ = "menu_items"

    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name          = Column(String(255), unique=True, nullable=False, index=True)  # dish name
    description   = Column(String(255), nullable=True)
    price         = Column(Numeric, nullable=False)
    calories      = Column(Integer, nullable=False)
    food_category = Column(String(255), nullable=False, index=True)

    # ingredients are joined from menu_item_resources
    menu_item_resources = relationship(
        "MenuItemResource",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )
    order_details = relationship(
        "OrderDetail",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )