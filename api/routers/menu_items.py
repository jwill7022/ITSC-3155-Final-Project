from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..services.menu_services import MenuService
from ..models.menu_items import FoodCategory
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Menu Items'],
    prefix="/menu_items",
)


@router.post("/", response_model=schema.MenuItems)
def create(request: schema.MenuItemsCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.MenuItems])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/search")
def search_menu_items(
        search_term: Optional[str] = Query(None, description="Search in name and description"),
        category: Optional[FoodCategory] = Query(None, description="Filter by food category"),
        min_price: Optional[float] = Query(None, description="Minimum price"),
        max_price: Optional[float] = Query(None, description="Maximum price"),
        sort_by: str = Query("name", description="Sort by: name, price_asc, price_desc, calories"),
        db: Session = Depends(get_db)
):
    """Search and filter menu items."""
    return MenuService.search_menu_items(
        db, search_term, category, min_price, max_price, sort_by
    )


@router.get("/{item_id}", response_model=schema.MenuItems)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.MenuItems)
def update(item_id: int, request: schema.MenuItemsUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)