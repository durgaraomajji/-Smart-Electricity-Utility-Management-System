from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.bill import Bill
from app.models.connection import Connection
from app.models.customer import Customer
from app.schemas.bill import BillGenerateRequest,BillResponse
from app.services.bill_service import BillService

router=APIRouter(prefix="/bills",tags=["Bills"])


@router.post("/generate",response_model=BillResponse,status_code=201)
def generate(data:BillGenerateRequest,db:Session=Depends(get_db),_=Depends(get_current_user)): return BillService.generate(db,data)

@router.get("",response_model=list[BillResponse])
def list_bills(billing_month:str|None=None,bill_status:str|None=None,min_amount:float|None=None,max_amount:float|None=None,page:int=1,limit:int=20,db:Session=Depends(get_db),_=Depends(get_current_user)):
    q=select(Bill)
    if billing_month:q=q.where(Bill.billing_month==billing_month)
    if bill_status:q=q.where(Bill.bill_status==bill_status)
    if min_amount is not None:q=q.where(Bill.total_amount>=min_amount)
    if max_amount is not None:q=q.where(Bill.total_amount<=max_amount)
    return db.scalars(q.offset((page-1)*limit).limit(limit)).all()

@router.get("/{bill_id}",response_model=BillResponse)
def get(bill_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    from fastapi import HTTPException
    obj=db.get(Bill,bill_id)
    if not obj: raise HTTPException(404,"Bill not found")
    return obj

@router.get("/customers/{customer_id}/bills",response_model=list[BillResponse])
def customer_bills(customer_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return db.scalars(select(Bill).join(Connection).where(Connection.customer_id==customer_id)).all()

@router.get("/connections/{connection_id}/bills",response_model=list[BillResponse])
def connection_bills(connection_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return db.scalars(select(Bill).where(Bill.connection_id==connection_id)).all()
