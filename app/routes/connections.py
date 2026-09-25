from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models.connection import Connection
from app.schemas.connection import ConnectionCreate,ConnectionUpdate,ConnectionResponse
from app.services.connection_service import ConnectionService
from app.utils.enums import ConnectionStatus

router=APIRouter(prefix="/connections",tags=["Connections"])


@router.post("",response_model=ConnectionResponse,status_code=201)
def create(data:ConnectionCreate,db:Session=Depends(get_db),_=Depends(get_current_user)): return ConnectionService.create(db,data)

@router.get("",response_model=list[ConnectionResponse])
def list_connections(status:str|None=None,connection_type:str|None=None,page:int=1,limit:int=20,db:Session=Depends(get_db),_=Depends(get_current_user)):
    q=select(Connection)
    if status:q=q.where(Connection.status==status)
    if connection_type:q=q.where(Connection.connection_type==connection_type)
    return db.scalars(q.offset((page-1)*limit).limit(limit)).all()

@router.get("/{connection_id}",response_model=ConnectionResponse)
def get(connection_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)): return ConnectionService.get(db,connection_id)

@router.put("/{connection_id}",response_model=ConnectionResponse)
def update(connection_id:int,data:ConnectionUpdate,db:Session=Depends(get_db),_=Depends(get_current_user)): return ConnectionService.update(db,connection_id,data)

@router.post("/{connection_id}/disconnect",response_model=ConnectionResponse)
def disconnect(connection_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    obj=ConnectionService.get(db,connection_id); obj.status=ConnectionStatus.DISCONNECTED.value; db.commit(); db.refresh(obj); return obj
