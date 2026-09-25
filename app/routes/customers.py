from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.customer_service import CustomerService

router=APIRouter(prefix="/customers",tags=["Customers"])


@router.post("",response_model=CustomerResponse,status_code=201)
def create(data:CustomerCreate,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return CustomerService.create(db,data)


@router.get("",response_model=list[CustomerResponse])
def list_customers(city:str|None=None,status:str|None=None,page:int=Query(1,ge=1),limit:int=Query(20,ge=1,le=100),db:Session=Depends(get_db),_=Depends(get_current_user)):
    q=select(Customer).where(Customer.is_deleted==False)
    if city: q=q.where(Customer.city==city)
    if status: q=q.where(Customer.status==status)
    return db.scalars(q.offset((page-1)*limit).limit(limit)).all()


@router.get("/{customer_id}",response_model=CustomerResponse)
def get(customer_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return CustomerService.get(db,customer_id)


@router.put("/{customer_id}",response_model=CustomerResponse)
def update(customer_id:int,data:CustomerUpdate,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return CustomerService.update(db,customer_id,data)


@router.delete("/{customer_id}")
def delete(customer_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    obj=CustomerService.get(db,customer_id); obj.is_deleted=True; db.commit()
    return {"message":"Customer deleted successfully"}
