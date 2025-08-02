from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, TypeVar, Generic, List, Optional, Any
from functools import wraps
from pydantic import BaseModel

# Define generic types
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def handle_db_errors(func):
    """Improved error handler with better error messages"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            # Extract more meaningful error information
            error_msg = str(e.orig) if hasattr(e, 'orig') and e.orig else str(e)

            # Handle common SQL errors with user-friendly messages
            if "Duplicate entry" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Resource already exists"
                )
            elif "foreign key constraint" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot complete operation due to related data"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Database error: {error_msg}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )

    return wrapper


class BaseCRUDController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @handle_db_errors
    def create(self, db: Session, request: CreateSchemaType) -> ModelType:
        obj_data = request.dict() if hasattr(request, 'dict') else request
        new_item = self.model(**obj_data)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @handle_db_errors
    def read_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    @handle_db_errors
    def read_one(self, db: Session, item_id: int) -> ModelType:
        item = db.query(self.model).filter(self.model.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} with id {item_id} not found"
            )
        return item

    @handle_db_errors
    def update(self, db: Session, item_id: int, request: UpdateSchemaType) -> ModelType:
        item = db.query(self.model).filter(self.model.id == item_id)
        if not item.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} with id {item_id} not found"
            )

        update_data = request.dict(exclude_unset=True) if hasattr(request, 'dict') else request
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()

    @handle_db_errors
    def delete(self, db: Session, item_id: int) -> Response:
        item = db.query(self.model).filter(self.model.id == item_id)
        if not item.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} with id {item_id} not found"
            )
        item.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @handle_db_errors
    def exists(self, db: Session, item_id: int) -> bool:
        """Check if item exists"""
        return db.query(self.model).filter(self.model.id == item_id).first() is not None

    @handle_db_errors
    def count(self, db: Session) -> int:
        """Get total count of items"""
        return db.query(self.model).count()