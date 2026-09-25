from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.tariff import Tariff
from app.schemas.tariff import TariffCreate,TariffUpdate,TariffResponse
from app.services.tariff_service import TariffService

router=APIRouter(prefix="/tariffs",tags=["Tariffs"])


@router.post("",response_model=TariffResponse,status_code=201)
def create(data:TariffCreate,db:Session=Depends(get_db),_=Depends(get_current_user)): return TariffService.create(db,data)

@router.get("",response_model=list[TariffResponse])
def list_tariffs(db:Session=Depends(get_db),_=Depends(get_current_user)): return db.scalars(select(Tariff)).all()

@router.put("/{tariff_id}",response_model=TariffResponse)
def update(tariff_id:int,data:TariffUpdate,db:Session=Depends(get_db),_=Depends(get_current_user)):
    obj=db.get(Tariff,tariff_id)
    if not obj: from fastapi import HTTPException; raise HTTPException(404,"Tariff not found")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@router.delete("/{tariff_id}")
def delete(tariff_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    obj=db.get(Tariff,tariff_id)
    if not obj: from fastapi import HTTPException; raise HTTPException(404,"Tariff not found")
    obj.status=False; db.commit(); return {"message":"Tariff deactivated"}
