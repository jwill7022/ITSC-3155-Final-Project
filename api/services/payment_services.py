from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict
from ..models.payments import Payment, PaymentType, PaymentStatus
from ..models.orders import Order, StatusType
from decimal import Decimal

class PaymentService:

    @staticmethod
    def process_payment(db: Session, order_id: int, payment_data: Dict) -> Payment:
        """ Process payment for an order"""
        try:
            #Get the order
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )

            #Check if order already has payment
            existing_payment = db.query(Payment).filter(Payment.order_id == order_id).first()
            if existing_payment:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Payment already exists for this order"
                )

            #Validate payment amount matches order total with proper type conversion
            if order.total_amount and abs(float(order.total_amount) - float(payment_data["amount"])) > 0.01:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Payment amount {payment_data['amount']} does not match order total {order.total_amount}"
                )

            #Create payment record
            payment = Payment(
                order_id=order_id,
                amount=payment_data["amount"],
                payment_type=payment_data["payment_type"],
                status=PaymentStatus.PENDING
            )

            db.add(payment)
            db.flush()

            #Simulation of payment processing
            #In actual implementation, this would interact with payment gateway
            payment_successful = PaymentService._simulate_payment_processing(payment_data)

            if payment_successful:
                payment.status = PaymentStatus.COMPLETED
                order.status = StatusType.CONFIRMED
            else:
                payment.status = PaymentStatus.FAILED

            db.commit()
            db.refresh(payment)

            return payment

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment processing failed: {str(e)}"
            )

    @staticmethod
    def _simulate_payment_processing(payment_data: Dict) -> bool:
        """
        Simulate payment gateway processing
        In real implementation, this would call actual payment service
        :param payment_data:
        :return:
        """
        #Simple simulation - reject if amount is exactly $31.55 (for testing purposes)
        if float(payment_data["amount"]) == 31.55:
            return False

        #Accept all other payments
        return True

    @staticmethod
    def get_payment_by_order(db: Session, order_id: int) -> Payment:
        try:
            payment = db.query(Payment).filter(Payment.order_id == order_id).first()
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found for this order"
                )
            return payment
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database error: {str(e)}"
            )