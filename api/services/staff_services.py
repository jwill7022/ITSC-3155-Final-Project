from sqlalchemy.orm import Session
from api.models.menu_item_ingredients import MenuItemIngredient
from api.models.resources import Resource


# this function gets and returns the ingredients needed for a particular menu item
def get_required_ingredients(db, menu_item_id, quantity):
    ingredients = db.query(MenuItemIngredient).join(Resource).filter(
        MenuItemIngredient.menu_item_id == menu_item_id
    ).all()

    return {
        ingredient.resource.item: ingredient.amount * quantity
        for ingredient in ingredients
    }