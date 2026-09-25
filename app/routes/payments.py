from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate,PaymentResponse
from app.services.payment_service import PaymentService

router=APIRouter(prefix="/payments",tags=["Payments"])


@router.post("/{bill_id}",response_model=PaymentResponse,status_code=201)
def create(bill_id:int,data:PaymentCreate,db:Session=Depends(get_db),_=Depends(get_current_user)): return PaymentService.create(db,bill_id,data)

@router.get("",response_model=list[PaymentResponse])
def list_payments(db:Session=Depends(get_db),_=Depends(get_current_user)): return db.scalars(select(Payment)).all()

@router.get("/{payment_id}",response_model=PaymentResponse)
def get(payment_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    from fastapi import HTTPException
    obj=db.get(Payment,payment_id)
    if not obj: raise HTTPException(404,"Payment not found")
    return obj

@router.get("/bill/{bill_id}",response_model=list[PaymentResponse])
def bill_payments(bill_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return db.scalars(select(Payment).where(Payment.bill_id==bill_id)).all()
