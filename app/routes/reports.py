from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.services.report_service import ReportService

router=APIRouter(prefix="/reports",tags=["Reports"])


@router.get("/monthly-revenue")
def monthly_revenue(month:str,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return ReportService.monthly_revenue(db,month)

@router.get("/daily-collection")
def daily_collection(date:str,db:Session=Depends(get_db),_=Depends(get_current_user)):
    from sqlalchemy import select,func
    from app.models.payment import Payment
    total=db.scalar(select(func.coalesce(func.sum(Payment.amount),0)).where(Payment.payment_date==date)) or 0
    return {"date":date,"collection":float(total)}

@router.get("/outstanding-payments")
def outstanding(db:Session=Depends(get_db),_=Depends(get_current_user)):
    from sqlalchemy import select
    from app.models.bill import Bill
    from app.utils.enums import BillStatus
    rows=db.scalars(select(Bill).where(Bill.bill_status.in_([BillStatus.PENDING.value,BillStatus.OVERDUE.value]))).all()
    return [{"bill_id":b.id,"amount":b.total_amount,"status":b.bill_status} for b in rows]
