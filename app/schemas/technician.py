from pydantic import BaseModel
from app.utils.enums import AvailabilityStatus


class TechnicianCreate(BaseModel):
    name: str
    employee_id: str
    phone: str
    specialization: str
    availability_status: AvailabilityStatus = AvailabilityStatus.AVAILABLE


class TechnicianResponse(TechnicianCreate):
    id: int
    model_config = {"from_attributes": True}


class TechnicianAvailabilityUpdate(BaseModel):
    availability_status: AvailabilityStatus
