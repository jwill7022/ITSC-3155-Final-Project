from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from api.models.menu_item_ingredients import MenuItemIngredient
from api.models.orders import Order, StatusType
from api.models.payments import Payment, PaymentStatus
from api.models.resources import Resource
from api.models import promotions as promotion_model


def calculate_daily_revenue(db, date):
    revenue = db.query(func.sum(Order.total_amount)).filter(
        func.date(Order.order_date) == date,
        Order.status == StatusType.COMPLETED  # Only count completed orders
    ).scalar()
    return float(revenue) if revenue else 0.0

# this function gets and returns the ingredients needed for a particular menu item
def get_required_ingredients(db, menu_item_id, quantity):
    ingredients = db.query(MenuItemIngredient).join(Resource).filter(
        MenuItemIngredient.menu_item_id == menu_item_id
    ).all()

    return {
        ingredient.resource.item: ingredient.amount * quantity
        for ingredient in ingredients
    }

def check_ingredient_availability(db, menu_item_id, quantity):
    required = get_required_ingredients(db, menu_item_id, quantity)
    shortages = []

    for ingredient_name, needed_amount in required.items():
        resource = db.query(Resource).filter(Resource.item == ingredient_name).first()
        if resource and resource.amount < needed_amount:
            shortages.append({
                "ingredient": ingredient_name,
                "needed": needed_amount,
                "available": resource.amount,
                "shortage": needed_amount - resource.amount
            })

    return shortages

# staff actions for promotions
def get_promotion_by_code(db: Session, promo_code: str):
    try:
        item = db.query(promotion_model.Promotion).filter(promotion_model.Promotion.code == promo_code).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update_promotion_by_code(db: Session, promo_code: str, request):
    try:
        item = db.query(promotion_model.Promotion).filter(promotion_model.Promotion.code == promo_code)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete_promotion_by_code(db: Session, promo_code: str):
    try:
        item = db.query(promotion_model.Promotion).filter(promotion_model.Promotion.code == promo_code)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)