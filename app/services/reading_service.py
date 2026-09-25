from sqlalchemy import select
from fastapi import HTTPException
from app.models.meter import Meter
from app.models.meter_reading import MeterReading
from app.utils.enums import MeterStatus


class ReadingService:
    @staticmethod
    def create(db, data):
        meter=db.get(Meter,data.meter_id)
        if not meter: raise HTTPException(404,"Meter not found")
        if meter.meter_status != MeterStatus.ACTIVE.value: raise HTTPException(400,"Only active meters can receive readings")
        duplicate=db.scalar(select(MeterReading).where(MeterReading.meter_id==data.meter_id, MeterReading.reading_date==data.reading_date))
        if duplicate: raise HTTPException(400,"Duplicate reading for this date")
        previous=meter.current_reading
        if data.current_reading < previous: raise HTTPException(400,"Current reading cannot be lower than previous reading")
        units=data.current_reading-previous
        obj=MeterReading(
            meter_id=data.meter_id, reading_date=data.reading_date,
            previous_reading=previous, current_reading=data.current_reading,
            units_consumed=units, reading_source=data.reading_source.value,
            remarks=data.remarks
        )
        meter.current_reading=data.current_reading
        db.add(obj); db.commit(); db.refresh(obj); return obj
