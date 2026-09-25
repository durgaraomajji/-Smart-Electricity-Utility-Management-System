from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.analytics import MonthlyConsumptionResponse,AnalyticsSummary
from app.services.analytics_service import AnalyticsService

router=APIRouter(prefix="/analytics",tags=["Analytics"])


@router.get("/connections/{connection_id}/monthly",response_model=list[MonthlyConsumptionResponse])
def monthly(connection_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return AnalyticsService.monthly(db,connection_id)

@router.get("/connections/{connection_id}/yearly",response_model=list[MonthlyConsumptionResponse])
def yearly(connection_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return AnalyticsService.monthly(db,connection_id)

@router.get("/connections/{connection_id}/usage")
def usage(connection_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    rows=AnalyticsService.monthly(db,connection_id)
    total=sum(x["units_consumed"] for x in rows)
    return {"connection_id":connection_id,"total_units":total,"months":rows}

@router.get("/highest-consuming")
def highest(db:Session=Depends(get_db),_=Depends(get_current_user)):
    from sqlalchemy import select,func
    from app.models.meter_reading import MeterReading
    from app.models.meter import Meter
    rows=db.execute(select(Meter.connection_id,func.sum(MeterReading.units_consumed).label("units")).join(Meter).group_by(Meter.connection_id).order_by(func.sum(MeterReading.units_consumed).desc()).limit(10)).all()
    return [{"connection_id":r[0],"units_consumed":float(r[1] or 0)} for r in rows]
