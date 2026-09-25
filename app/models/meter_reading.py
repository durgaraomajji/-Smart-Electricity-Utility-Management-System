from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, Enum as SAEnum, Float, String, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.utils.enums import ReadingSource


class MeterReading(Base):
    __tablename__ = "meter_readings"
    __table_args__ = (
        UniqueConstraint("meter_id", "reading_date", name="uq_meter_reading_date"),
        Index("ix_meter_readings_meter_date", "meter_id", "reading_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    meter_id: Mapped[int] = mapped_column(ForeignKey("meters.id"), index=True)
    reading_date: Mapped[date] = mapped_column(Date)
    previous_reading: Mapped[float] = mapped_column(Float)
    current_reading: Mapped[float] = mapped_column(Float)
    units_consumed: Mapped[float] = mapped_column(Float)
    reading_source: Mapped[str] = mapped_column(SAEnum(ReadingSource))
    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    meter = relationship("Meter", back_populates="readings")
