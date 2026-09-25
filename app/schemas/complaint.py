from datetime import datetime
from pydantic import BaseModel, Field
from app.utils.enums import ComplaintType, Priority, ComplaintStatus


class ComplaintCreate(BaseModel):
    customer_id: int
    connection_id: int | None = None
    complaint_type: ComplaintType
    description: str = Field(min_length=5)
    priority: Priority = Priority.MEDIUM


class ComplaintResponse(ComplaintCreate):
    id: int
    assigned_to: int | None
    status: ComplaintStatus
    created_at: datetime
    resolved_at: datetime | None
    model_config = {"from_attributes": True}


class ComplaintAssignRequest(BaseModel):
    technician_id: int


class ComplaintStatusRequest(BaseModel):
    status: ComplaintStatus
    remarks: str | None = None
