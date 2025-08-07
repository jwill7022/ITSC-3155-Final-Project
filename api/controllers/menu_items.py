from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import menu_items as model
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from ..models.reviews import Reviews
from ..models.menu_item_ingredients import MenuItemIngredient
from ..models.resources import Resource


def create(db: Session, request):
    # Check for duplicate menu item name
    existing_item = db.query(model.MenuItem).filter(model.MenuItem.name == request.name).first()
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,  # Changed to 409 for consistency
            detail=f"Menu item with name '{request.name}' already exists"
        )

    # Handle food_category enum conversion if needed
    food_category = request.food_category
    if isinstance(food_category, str):
        try:
            food_category = model.FoodCategory(food_category.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid food category: {food_category}"
            )

    new_item = model.MenuItem(
        name=request.name,
        description=request.description,
        price=request.price,
        calories=request.calories,
        food_category=food_category,
        is_available=getattr(request, 'is_available', True)
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


# Rest of the functions remain the same...
def read_all(db: Session, skip: int = 0, limit: int = 100, available_only: bool = True):
    try:
        query = db.query(model.MenuItem)
        if available_only:
            query = query.filter(model.MenuItem.is_available == True)
        result = query.offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def get_nutrition_info(db: Session, item_id: int):
    """Get nutrition and ingredient information for a menu item"""
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")

        ingredients = db.query(MenuItemIngredient, Resource).join(
            Resource, MenuItemIngredient.resource_id == Resource.id
        ).filter(MenuItemIngredient.menu_item_id == item_id).all()

        ingredient_list = [
            {
                "name": resource.item,
                "amount": ingredient.amount
            }
            for ingredient, resource in ingredients
        ]

        return {
            "menu_item": {
                "id": item.id,
                "name": item.name,
                "calories": item.calories,
                "food_category": item.food_category.value
            },
            "ingredients": ingredient_list
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update_availability(db: Session, item_id: int, available: bool):
    """Toggle menu item availability"""
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        item.update({"is_available": available}, synchronize_session=False)
        db.commit()
        return item.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update(db: Session, item_id, request):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)