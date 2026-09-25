from sqlalchemy import select
from fastapi import HTTPException
from app.models.payment import Payment
from app.models.bill import Bill
from app.utils.enums import PaymentStatus, BillStatus


class PaymentService:
    @staticmethod
    def create(db,bill_id,data):
        bill=db.get(Bill,bill_id)
        if not bill: raise HTTPException(404,"Bill not found")
        if data.amount > bill.total_amount: raise HTTPException(400,"Payment cannot exceed bill amount")
        if db.scalar(select(Payment).where(Payment.transaction_id==data.transaction_id)):
            raise HTTPException(400,"Duplicate transaction")
        obj=Payment(bill_id=bill_id, amount=data.amount, payment_method=data.payment_method.value,
                    transaction_id=data.transaction_id, payment_date=data.payment_date,
                    payment_status=PaymentStatus.SUCCESS.value)
        if data.amount == bill.total_amount:
            bill.bill_status=BillStatus.PAID.value
        db.add(obj); db.commit(); db.refresh(obj); return obj
