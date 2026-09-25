from datetime import datetime
from sqlalchemy import String, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.utils.enums import AvailabilityStatus


class Technician(Base):
    __tablename__ = "technicians"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    employee_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(30))
    specialization: Mapped[str] = mapped_column(String(120))
    availability_status: Mapped[str] = mapped_column(
        SAEnum(AvailabilityStatus),
        default=AvailabilityStatus.AVAILABLE,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    complaints = relationship("Complaint", back_populates="technician")
