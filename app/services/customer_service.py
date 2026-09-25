from sqlalchemy import select
from fastapi import HTTPException
from app.models.customer import Customer


class CustomerService:
    @staticmethod
    def create(db, data):
        if db.scalar(select(Customer).where(Customer.customer_number == data.customer_number)):
            raise HTTPException(400, "Customer number already exists")
        if db.scalar(select(Customer).where(Customer.email == data.email)):
            raise HTTPException(400, "Email already exists")
        obj = Customer(**data.model_dump())
        db.add(obj); db.commit(); db.refresh(obj); return obj

    @staticmethod
    def get(db, customer_id):
        obj = db.get(Customer, customer_id)
        if not obj or obj.is_deleted: raise HTTPException(404, "Customer not found")
        return obj

    @staticmethod
    def update(db, customer_id, data):
        obj = CustomerService.get(db, customer_id)
        for k,v in data.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
        db.commit(); db.refresh(obj); return obj
