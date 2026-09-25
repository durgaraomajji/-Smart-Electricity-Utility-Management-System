from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SAEnum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.utils.enums import MeterStatus


class Meter(Base):
    __tablename__ = "meters"
    id: Mapped[int] = mapped_column(primary_key=True)
    connection_id: Mapped[int] = mapped_column(ForeignKey("connections.id"), index=True)
    meter_number: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    meter_type: Mapped[str] = mapped_column(String(80))
    installation_date: Mapped[date] = mapped_column(Date)
    initial_reading: Mapped[float] = mapped_column(Float, default=0)
    current_reading: Mapped[float] = mapped_column(Float, default=0)
    meter_status: Mapped[str] = mapped_column(SAEnum(MeterStatus), default=MeterStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    connection = relationship("Connection", back_populates="meters")
    readings = relationship("MeterReading", back_populates="meter")
