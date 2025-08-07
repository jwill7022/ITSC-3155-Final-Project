from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..dependencies.database import get_db

# holds common actions made by administrators

router = APIRouter(
    tags=['Administrator Actions'],
    prefix="/administrator_actions",
)

@router.delete("/purge-db")
def purge_database(db: Session = Depends(get_db), confirm: str = None):
    # Administrator action to purge all data from the database
    # User warning:
    """
    DANGER: This will delete ALL data from the database!
    Must pass confirm='DELETE_ALL_DATA' to execute.
    :param db: restaurant_order_system
    :param confirm:
    :return:
    """
    if confirm != "DELETE_ALL_DATA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must pass confirm='DELETE_ALL_DATA' to execute."
        )

    try:
        #Temporarily disable foreign key checks
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        #Get all table names
        tables = [
            "payments", "order_details", "menu_item_ingredients",
            "reviews", "orders", "customers", "menu_items",
            "resources", "promotions"
        ]

        #Delete tables in proper order
        for table in tables:
            db.execute(text(f"DELETE FROM {table}"))
            db.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))

        #Re-enable foreign key checks
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        db.commit()
        return {"message": "Database purged successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to purge database: {str(e)}"
        )