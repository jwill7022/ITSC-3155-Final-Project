from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    value = Column(Integer, nullable=False) # 1-5gi
    review_text = Column(String(500))
    created_at = Column(DateTime, default=str(datetime.now()))

    customer = relationship("Customer", back_populates="ratings")