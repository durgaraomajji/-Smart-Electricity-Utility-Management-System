from sqlalchemy import select
from fastapi import HTTPException
from app.models.connection import Connection
from app.models.customer import Customer
from app.utils.enums import CustomerStatus, ConnectionStatus


class ConnectionService:
    @staticmethod
    def create(db, data):
        if db.scalar(select(Connection).where(Connection.connection_number == data.connection_number)):
            raise HTTPException(400, "Connection number already exists")
        customer = db.get(Customer, data.customer_id)
        if not customer or customer.is_deleted: raise HTTPException(404, "Customer not found")
        obj = Connection(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

    @staticmethod
    def get(db, id):
        obj=db.get(Connection,id)
        if not obj: raise HTTPException(404,"Connection not found")
        return obj

    @staticmethod
    def update(db,id,data):
        obj=ConnectionService.get(db,id)
        for k,v in data.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
        db.commit(); db.refresh(obj); return obj
