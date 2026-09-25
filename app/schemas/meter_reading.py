from datetime import date
from pydantic import BaseModel, Field
from app.utils.enums import ReadingSource


class MeterReadingCreate(BaseModel):
    meter_id: int
    reading_date: date
    current_reading: float = Field(ge=0)
    reading_source: ReadingSource
    remarks: str | None = None


class MeterReadingResponse(BaseModel):
    id: int
    meter_id: int
    reading_date: date
    previous_reading: float
    current_reading: float
    units_consumed: float
    reading_source: ReadingSource
    remarks: str | None

    model_config = {"from_attributes": True}
