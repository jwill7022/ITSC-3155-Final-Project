from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import payments as controller
from ..schemas import payments as schema
from ..dependencies.database import get_db
from ..services.payment_services import PaymentService

router = APIRouter(
    tags=['Payments'],
    prefix="/payments",
)


@router.post("/", response_model=schema.Payment)
def create(request: schema.PaymentCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.post("/process/{order_id}", response_model=schema.Payment)
def process_payment(
        order_id: int,
        payment_data: dict, #{"amount": 25.50, "payment_type": "credit_card"}
        db: Session = Depends(get_db)
):
    """Process payment for an order"""
    return PaymentService.process_payment(db, order_id, payment_data)

@router.get("/order/{order_id}", response_model=schema.Payment)
def get_payment_by_order(order_id: int, db: Session = Depends(get_db)):
    """Get payment details for an order"""
    return PaymentService.get_payment_by_order(db, order_id)

@router.get("/", response_model=list[schema.Payment])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Payment)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.Payment)
def update(item_id: int, request: schema.PaymentUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
