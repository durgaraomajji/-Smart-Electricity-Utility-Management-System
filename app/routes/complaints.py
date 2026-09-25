from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate,ComplaintResponse,ComplaintAssignRequest,ComplaintStatusRequest
from app.services.complaint_service import ComplaintService

router=APIRouter(prefix="/complaints",tags=["Complaints"])


@router.post("",response_model=ComplaintResponse,status_code=201)
def create(data:ComplaintCreate,db:Session=Depends(get_db),_=Depends(get_current_user)): return ComplaintService.create(db,data)

@router.get("",response_model=list[ComplaintResponse])
def list_complaints(priority:str|None=None,status:str|None=None,complaint_type:str|None=None,assigned_to:int|None=None,db:Session=Depends(get_db),_=Depends(get_current_user)):
    q=select(Complaint)
    if priority:q=q.where(Complaint.priority==priority)
    if status:q=q.where(Complaint.status==status)
    if complaint_type:q=q.where(Complaint.complaint_type==complaint_type)
    if assigned_to:q=q.where(Complaint.assigned_to==assigned_to)
    return db.scalars(q).all()

@router.get("/{complaint_id}",response_model=ComplaintResponse)
def get(complaint_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    from fastapi import HTTPException
    obj=db.get(Complaint,complaint_id)
    if not obj: raise HTTPException(404,"Complaint not found")
    return obj

@router.put("/{complaint_id}/assign",response_model=ComplaintResponse)
def assign(complaint_id:int,data:ComplaintAssignRequest,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return ComplaintService.assign(db,complaint_id,data.technician_id)

@router.put("/{complaint_id}/status",response_model=ComplaintResponse)
def update_status(complaint_id:int,data:ComplaintStatusRequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return ComplaintService.status(db,complaint_id,data.status,current_user.id,data.remarks)
