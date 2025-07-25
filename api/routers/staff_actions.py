from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..services import staff_services
from ..schemas import menu_items as schema
from ..dependencies.database import engine, get_db

# holds common actions made by the customer

router = APIRouter(
    tags=['Staff Actions'],
    prefix="/staff_actions",
)

@router.get("/")
def view_ingredients(menu_item_id: int, quantity: int, db: Session = Depends(get_db)):
    return staff_services.get_required_ingredients(db, menu_item_id, quantity)