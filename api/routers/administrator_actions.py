from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..dependencies.database import get_db

# holds common actions made by administrators

router = APIRouter(
    tags=['Administrator Actions'],
    prefix="/administrator_actions",
)

@router.delete("/purge-db")
def purge_database(db: Session = Depends(get_db)):
    # Administrator action to purge all data from the database
    try:
        from ..dependencies.database import Base
        
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        
        db.commit()
        return {"message": "Database purged successfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"Failed to purge database: {str(e)}"}