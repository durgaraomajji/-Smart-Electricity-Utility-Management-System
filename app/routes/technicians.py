from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.technician import Technician
from app.schemas.technician import TechnicianCreate,TechnicianResponse,TechnicianAvailabilityUpdate
from app.services.technician_service import TechnicianService

router=APIRouter(prefix="/technicians",tags=["Technicians"])


@router.post("",response_model=TechnicianResponse,status_code=201)
def create(data:TechnicianCreate,db:Session=Depends(get_db),_=Depends(get_current_user)): return TechnicianService.create(db,data)

@router.get("",response_model=list[TechnicianResponse])
def list_technicians(db:Session=Depends(get_db),_=Depends(get_current_user)): return db.scalars(select(Technician)).all()

@router.get("/{technician_id}",response_model=TechnicianResponse)
def get(technician_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    from fastapi import HTTPException
    obj=db.get(Technician,technician_id)
    if not obj: raise HTTPException(404,"Technician not found")
    return obj

@router.put("/{technician_id}/availability",response_model=TechnicianResponse)
def availability(technician_id:int,data:TechnicianAvailabilityUpdate,db:Session=Depends(get_db),_=Depends(get_current_user)):
    from fastapi import HTTPException
    obj=db.get(Technician,technician_id)
    if not obj: raise HTTPException(404,"Technician not found")
    obj.availability_status=data.availability_status.value; db.commit(); db.refresh(obj); return obj
