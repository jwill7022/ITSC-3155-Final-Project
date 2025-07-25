from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Payment(Base):
        __tablename__ = "payments"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
        payment_date = Column(DATETIME, nullable=False, default=str(datetime.now()))
        amount = Column(Float, nullable=False)
        status = Column(String(50))
        payment_type = Column(String(50))

        order = relationship("Order", back_populates="payments")