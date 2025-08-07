from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    discount_percent = Column(Integer, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())