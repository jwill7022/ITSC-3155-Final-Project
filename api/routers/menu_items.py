from fastapi import APIRouter, Depends, Query, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Optional, List
from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..services.menu_services import MenuService
from ..models.menu_items import FoodCategory
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Menu Items'],
    prefix="/menu_items",
    responses={
        404: {"description": "Menu item not found"},
        400: {"description": "Invalid input data"}
    }
)


@router.post(
    "/",
    response_model=schema.MenuItemsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create menu item",
    description="Add a new item to the menu"
)
def create_menu_item(
        request: schema.MenuItemsCreate,
        db: Session = Depends(get_db)
) -> schema.MenuItemsResponse:
    """
    Create a new menu item:

    - **name**: Unique item name (2-100 characters)
    - **description**: Item description (optional, max 500 characters)
    - **price**: Price in USD (must be > 0)
    - **calories**: Calories per serving (0-5000)
    - **food_category**: Category (vegetarian, vegan, gluten_free, regular, keto, low_carb
    - **is_available**: Whether item is currently available (default: true)
    :param request:
    :param db:
    :return:
    """
    return controller.create(db=db, request=request)


@router.get(
    "/",
    response_model=list[schema.MenuItemsResponse],
    summary="Get all menu items",
    description="Retrieve all menu items with filtering and sorting options"
)
def get_menu_items(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        available_only: bool = Query(True, description="Show only available items"),
        db: Session = Depends(get_db)
) -> List[schema.MenuItemsResponse]:
    return controller.read_all(db, skip, limit, available_only)

@router.get(
    "/search",
    response_model=List[schema.MenuItemsResponse],
    summary="Search menu items",
    description="Advanced search and filtering of menu items"
)
def search_menu_items(
        search_term: Optional[str] = Query(None, description="Search in name and description"),
        category: Optional[FoodCategory] = Query(None, description="Filter by food category"),
        min_price: Optional[float] = Query(None, description="Minimum price"),
        max_price: Optional[float] = Query(None, description="Maximum price"),
        max_calories: Optional[int] = Query(None, ge=0, description="Maximum calories filter"),
        sort_by: str = Query("name", pattern="^(name|price_asc|price_desc|calories|rating)$"),
        available_only: bool = Query(True, description="Show only available items"),
        db: Session = Depends(get_db)
):
    """
    Menu search with multiple filters:

    - **search_term**: Search in item name and description
    - **category**: Filter by dietary category
    - **min_price/max_price**: Price range filtering
    - **max_calories**: Maximum calories filter
    - **sort_by**: Sort by name, price_asc, price_desc, calories, or rating
    - **available_only**: Show only available items
    :param search_term:
    :param category:
    :param min_price:
    :param max_price:
    :param sort_by:
    :param available_only:
    :param db:
    :return:
    """
    if max_price and min_price and max_price < min_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="max_price must be greater than min_price"
        )

    return MenuService.search_menu_items(
        db, search_term, category, min_price, max_price, max_calories, sort_by, available_only
    )


@router.get(
    "/{item_id}",
    response_model=schema.MenuItemsResponse,
    summary="Get menu item by ID"
)
def get_menu_item(
        item_id: int = Path(..., gt=0, description="The ID of the menu item"),
        db: Session = Depends(get_db)
) -> schema.MenuItemsResponse:
    """
    Get detailed information about a specific menu item
    :param item_id:
    :param db:
    :return:
    """
    return controller.read_one(db, item_id=item_id)

@router.get(
    "/{item_id}/nutrition",
    summary="Get nutrition information",
    description="Get detailed nutrition information for a menu item"
)
def get_nutrition_info(
        item_id: int = Path(..., gt=0),
        db: Session = Depends(get_db)
):
    """Get nutrition and ingredient information for a menu item"""
    return controller.get_nutrition_info(db, item_id)

@router.put(
    "/{item_id}",
    response_model=schema.MenuItemsResponse,
    summary="Update menu item"
)
def update_menu_item(
    request: schema.MenuItemsUpdate,
    item_id: int = Path(..., gt=0, description="The id of the menu item"),
    db: Session = Depends(get_db)
) -> schema.MenuItemsResponse:
    """Update menu item information"""
    return controller.update(db=db, request=request, item_id=item_id)

@router.patch(
    "/{item_id}/availability",
    response_model=schema.MenuItemsResponse,
    summary="Toggle item availability"
)
def toggle_availability(
        item_id: int = Path(..., gt=0, description="The id of the menu item"),
        available: bool = Query(..., description="Set availability status"),
        db: Session = Depends(get_db)
) -> schema.MenuItemsResponse:
    """Toggle menu item availability without updating other fields"""
    return controller.update_availability(db, item_id, available)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete menu item"
)
def delete_menu_item(
        item_id: int = Path(..., gt=0, description="The id of the menu item"),
        db: Session = Depends(get_db)
):
    """Delete menu item (only if not in any orders)"""
    return controller.delete(db=db, item_id=item_id)