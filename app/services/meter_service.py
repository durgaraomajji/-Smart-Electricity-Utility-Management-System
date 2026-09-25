from sqlalchemy import select
from fastapi import HTTPException
from app.models.meter import Meter
from app.models.connection import Connection
from app.utils.enums import MeterStatus, ConnectionStatus


class MeterService:
    @staticmethod
    def create(db, data):
        if db.scalar(select(Meter).where(Meter.meter_number == data.meter_number)):
            raise HTTPException(400, "Meter number already exists")
        c=db.get(Connection,data.connection_id)
        if not c: raise HTTPException(404,"Connection not found")
        if c.status == ConnectionStatus.DISCONNECTED.value: raise HTTPException(400,"Disconnected connection")
        active=db.scalar(select(Meter).where(Meter.connection_id==data.connection_id, Meter.meter_status==MeterStatus.ACTIVE.value))
        if active: raise HTTPException(400,"Connection already has an active meter")
        obj=Meter(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

    @staticmethod
    def get(db,id):
        obj=db.get(Meter,id)
        if not obj: raise HTTPException(404,"Meter not found")
        return obj
