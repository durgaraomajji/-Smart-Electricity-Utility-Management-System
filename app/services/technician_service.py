from sqlalchemy import select
from fastapi import HTTPException
from app.models.technician import Technician


class TechnicianService:
    @staticmethod
    def create(db,data):
        if db.scalar(select(Technician).where(Technician.employee_id==data.employee_id)):
            raise HTTPException(400,"Employee ID already exists")
        obj=Technician(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj
