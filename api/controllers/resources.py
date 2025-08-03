from typing import List, Dict

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import resources as model
from ..schemas import resources as schema
from .base_controller import BaseCRUDController
from sqlalchemy.exc import SQLAlchemyError


class ResourceController(BaseCRUDController[model.Resource, schema.ResourceCreate, schema.ResourceUpdate]):
    def __init__(self):
        super().__init__(model.Resource)

    def create(self, db: Session, request: schema.ResourceCreate) -> model.Resource:
        """Override create to check for duplicate resource names"""
        try:
            # Check for duplicate resource item
            existing_resource = db.query(self.model).filter(self.model.item == request.item).first()
            if existing_resource:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Resource '{request.item}' already exists"
                )

            return super().create(db, request)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create resource: {str(e)}"
            )

    def get_low_stock_items(self, db: Session, threshold: int = 10):
        """Get resources below stock threshold"""
        try:
            return db.query(self.model).filter(self.model.amount <= threshold).all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get low stock items: {str(e)}"
            )

    def bulk_update_stock(self, db: Session, updates: List[Dict[str, int]]):
        """Bulk update stock levels"""
        try:
            updated_items = []
            for update in updates:
                resource_id = update.get('resource_id')
                new_amount = update.get('amount')

                if resource_id and new_amount is not None:
                    resource = db.query(self.model).filter(self.model.id == resource_id).first()
                    if resource:
                        resource.amount = new_amount
                        updated_items.append(resource)

            db.commit()
            return updated_items
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bulk update failed: {str(e)}"
            )


# Create controller instance
resource_controller = ResourceController()


# Function-based interface
def create(db: Session, request: schema.ResourceCreate):
    return resource_controller.create(db, request)


def read_all(db: Session):
    return resource_controller.read_all(db)


def read_one(db: Session, item_id: int):
    return resource_controller.read_one(db, item_id)


def update(db: Session, item_id: int, request: schema.ResourceUpdate):
    return resource_controller.update(db, item_id, request)


def delete(db: Session, item_id: int):
    return resource_controller.delete(db, item_id)


def get_low_stock_items(db: Session, threshold: int = 10):
    return resource_controller.get_low_stock_items(db, threshold)


def bulk_update_stock(db: Session, updates: List[Dict[str, int]]):
    return resource_controller.bulk_update_stock(db, updates)