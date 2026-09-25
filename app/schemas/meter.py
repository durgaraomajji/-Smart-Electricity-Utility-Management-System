from datetime import date
from pydantic import BaseModel, Field
from app.utils.enums import MeterStatus


class MeterCreate(BaseModel):
    connection_id: int
    meter_number: str
    meter_type: str
    installation_date: date
    initial_reading: float = Field(ge=0)
    current_reading: float = Field(ge=0)
    meter_status: MeterStatus = MeterStatus.ACTIVE


class MeterUpdate(BaseModel):
    current_reading: float | None = Field(default=None, ge=0)
    meter_status: MeterStatus | None = None


class MeterResponse(MeterCreate):
    id: int
    model_config = {"from_attributes": True}
