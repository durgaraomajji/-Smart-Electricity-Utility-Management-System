from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.service_request import ServiceRequest
from app.schemas.service_request import ServiceRequestCreate,ServiceRequestResponse
from app.services.service_request_service import ServiceRequestService
from app.utils.enums import ServiceRequestStatus

router=APIRouter(prefix="/service-requests",tags=["Service Requests"])


@router.post("",response_model=ServiceRequestResponse,status_code=201)
def create(data:ServiceRequestCreate,db:Session=Depends(get_db),_=Depends(get_current_user)): return ServiceRequestService.create(db,data)

@router.get("",response_model=list[ServiceRequestResponse])
def list_requests(db:Session=Depends(get_db),_=Depends(get_current_user)): return db.scalars(select(ServiceRequest)).all()

@router.get("/{request_id}",response_model=ServiceRequestResponse)
def get(request_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    from fastapi import HTTPException
    obj=db.get(ServiceRequest,request_id)
    if not obj: raise HTTPException(404,"Service request not found")
    return obj

def set_status(request_id, status, db):
    from fastapi import HTTPException
    obj=db.get(ServiceRequest,request_id)
    if not obj: raise HTTPException(404,"Service request not found")
    obj.status=status; db.commit(); db.refresh(obj); return obj

@router.put("/{request_id}/approve",response_model=ServiceRequestResponse)
def approve(request_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)): return set_status(request_id,ServiceRequestStatus.APPROVED.value,db)

@router.put("/{request_id}/reject",response_model=ServiceRequestResponse)
def reject(request_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)): return set_status(request_id,ServiceRequestStatus.REJECTED.value,db)

@router.put("/{request_id}/complete",response_model=ServiceRequestResponse)
def complete(request_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)): return set_status(request_id,ServiceRequestStatus.COMPLETED.value,db)
