from datetime import date
from pydantic import BaseModel, Field
from app.utils.enums import ServiceRequestType, ServiceRequestStatus


class ServiceRequestCreate(BaseModel):
    customer_id: int
    connection_id: int | None = None
    request_type: ServiceRequestType
    description: str = Field(min_length=5)
    requested_date: date


class ServiceRequestResponse(ServiceRequestCreate):
    id: int
    status: ServiceRequestStatus
    model_config = {"from_attributes": True}
