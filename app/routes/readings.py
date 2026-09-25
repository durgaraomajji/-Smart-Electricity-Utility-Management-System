from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.meter_reading import MeterReading
from app.models.meter import Meter
from app.models.connection import Connection
from app.schemas.meter_reading import MeterReadingCreate,MeterReadingResponse
from app.services.reading_service import ReadingService

router=APIRouter(tags=["Meter Readings"])


@router.post("/meter-readings",response_model=MeterReadingResponse,status_code=201)
def create(data:MeterReadingCreate,db:Session=Depends(get_db),_=Depends(get_current_user)): return ReadingService.create(db,data)

@router.get("/meter-readings",response_model=list[MeterReadingResponse])
def list_readings(db:Session=Depends(get_db),_=Depends(get_current_user)): return db.scalars(select(MeterReading)).all()

@router.get("/meters/{meter_id}/readings",response_model=list[MeterReadingResponse])
def meter_readings(meter_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)): return db.scalars(select(MeterReading).where(MeterReading.meter_id==meter_id)).all()

@router.get("/connections/{connection_id}/readings",response_model=list[MeterReadingResponse])
def connection_readings(connection_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return db.scalars(select(MeterReading).join(Meter).where(Meter.connection_id==connection_id)).all()
