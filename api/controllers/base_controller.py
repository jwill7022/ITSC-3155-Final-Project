from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, Any
from functools import wraps

def handle_db_errors(func):
    #Responsible for handling SQLAlchemy errors consistently
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            error = str(e.__dict__.get('orig', str(e)))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return wrapper

class BaseCRUDController:
    def __init__(self, model: Type[Any]):
        self.model = model

    @handle_db_errors
    def create(self, db: Session, request):
        new_item = self.model(**request.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @handle_db_errors
    def read_all(self, db: Session):
        return db.query(self.model).all()

    @handle_db_errors
    def read_one(self, db: Session, item_id: int):
        item = db.query(self.model).filter(self.model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found.")
        return item

    @handle_db_errors
    def update(self, db: Session, item_id: int, request):
        item = db.query(self.model).filter(self.model.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found.")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()

    @handle_db_errors
    def delete(self, db: Session, item_id: int):
        item = db.query(self.model).filter(self.model.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found.")
        item.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)