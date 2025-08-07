from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import promotions as model
from sqlalchemy.exc import SQLAlchemyError
from .base_controller import BaseCRUDController, handle_db_errors


class PromotionController(BaseCRUDController):
    def __init__(self):
        super().__init__(model.Promotion)

    @handle_db_errors
    def create(self, db: Session, request):
        # Check for duplicate promotion code
        existing_promo = db.query(model.Promotion).filter(
            model.Promotion.code == request.code
        ).first()
        if existing_promo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Promotion code '{request.code}' already exists"
            )

        return super().create(db, request)


# Create controller instance
promotion_controller = PromotionController()


def create(db: Session, request):
    return promotion_controller.create(db, request)


def read_all(db: Session):
    return promotion_controller.read_all(db)


def read_one(db: Session, item_id):
    return promotion_controller.read_one(db, item_id)


def update(db: Session, item_id, request):
    return promotion_controller.update(db, item_id, request)


def delete(db: Session, item_id):
    return promotion_controller.delete(db, item_id)
