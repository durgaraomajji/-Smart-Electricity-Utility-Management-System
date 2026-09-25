from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.meter import Meter
from app.schemas.meter import MeterCreate,MeterUpdate,MeterResponse
from app.services.meter_service import MeterService
from app.utils.enums import MeterStatus

router=APIRouter(prefix="/meters",tags=["Meters"])


@router.post("",response_model=MeterResponse,status_code=201)
def create(data:MeterCreate,db:Session=Depends(get_db),_=Depends(get_current_user)): return MeterService.create(db,data)

@router.get("",response_model=list[MeterResponse])
def list_meters(db:Session=Depends(get_db),_=Depends(get_current_user)): return db.scalars(select(Meter)).all()

@router.get("/{meter_id}",response_model=MeterResponse)
def get(meter_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)): return MeterService.get(db,meter_id)

@router.put("/{meter_id}",response_model=MeterResponse)
def update(meter_id:int,data:MeterUpdate,db:Session=Depends(get_db),_=Depends(get_current_user)):
    obj=MeterService.get(db,meter_id)
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@router.post("/{meter_id}/replace",response_model=MeterResponse)
def replace(meter_id:int,data:MeterCreate,db:Session=Depends(get_db),_=Depends(get_current_user)):
    old=MeterService.get(db,meter_id); old.meter_status=MeterStatus.REMOVED.value
    new=MeterService.create(db,data); return new
