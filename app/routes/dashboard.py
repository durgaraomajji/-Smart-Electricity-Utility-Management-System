from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router=APIRouter(prefix="/dashboard",tags=["Dashboard"])


@router.get("",response_model=DashboardResponse)
def dashboard(billing_month:str|None=None,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return DashboardService.get(db,billing_month)
