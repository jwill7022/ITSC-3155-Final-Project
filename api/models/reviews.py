from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False) # 1-5
    review_text = Column(String(500))
    created_at = Column(DateTime, default=str(datetime.now()))