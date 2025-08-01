from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from ..models.menu_item_ingredients import MenuItemIngredient
from ..models.resources import Resource
from ..models.order_details import OrderDetail
from typing import Dict, List

class InventoryService:

    @staticmethod
    def check_availability(db: Session, order_items: List[Dict]) -> Dict:
        """
        Check if all items in order can be fulfilled with current inventory
        order_items: [{"menu_item_id: 1, "quantity": 2}, ...]
        :param db:
        :param order_items:
        :return:
        """
        try:
            availability = {}
            insufficient_items = []

            for item in order_items:
                menu_item_id = item["menu_item_id"]
                quantity = item["quantity"]

                #Get required ingredients for this menu item
                ingredients = db.query(MenuItemIngredient).join(Resource).filter(
                    MenuItemIngredient.menu_item_id == menu_item_id
                ).all()

                item_available = True
                required_ingredients = {}

                for ingredient in ingredients:
                    required_amount = ingredient.amount * quantity
                    available_amount = ingredient.resource.amount

                    required_ingredients[ingredient.resource.item] = {
                        "required": required_amount,
                        "available": available_amount,
                        "sufficient": available_amount >= required_amount
                    }

                    if available_amount < required_amount:
                        item_available = False

                availability[menu_item_id] = {
                    "available": item_available,
                    "ingredients": required_ingredients
                }

                if not item_available:
                    insufficient_items.append(menu_item_id)

            return {
                "all available": len(insufficient_items) == 0,
                "insufficient items": insufficient_items,
                "details": availability
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )


    @staticmethod
    def deduct_inventory(db: Session, order_items: List[Dict]) -> bool:
        """
        Deduct inventory after order confirmation
        :param db:
        :param order_items:
        :return:
        """
        try:
            for item in order_items:
                menu_item_id = item["menu_item_id"]
                quantity = item["quantity"]

                ingredients = db.query(MenuItemIngredient).join(Resource).filter(
                    MenuItemIngredient.menu_item_id == menu_item_id
                ).all()

                for ingredient in ingredients:
                    required_amount = ingredient.amount * quantity
                    resource = ingredient.resource
                    resource.amount -= required_amount

                    if resource.amount < 0:
                        db.rollback()
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Insufficient inventory for {resource.item}"
                        )

            db.commit()
            return True

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to deduct inventory: {str(e)}"
            )

    @staticmethod
    def get_low_stock_items(db: Session, threshold: int = 10) -> List[Dict]:
        """
        Get items with low stock
        :param db:
        :param threshold:
        :return:
        """
        try:
            low_stock = db.query(Resource).filter(Resource.amount <= threshold).all()
            return [
                {
                    "id": item.id,
                    "item": item.item,
                    "current_amount": item.amount,
                    "threshold": threshold
                }
                for item in low_stock
            ]
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )