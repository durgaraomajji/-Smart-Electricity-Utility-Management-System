from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.utils.enums import ServiceRequestType, ServiceRequestStatus


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    connection_id: Mapped[int | None] = mapped_column(ForeignKey("connections.id"), nullable=True)
    request_type: Mapped[str] = mapped_column(SAEnum(ServiceRequestType))
    description: Mapped[str] = mapped_column(Text)
    requested_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(SAEnum(ServiceRequestStatus), default=ServiceRequestStatus.SUBMITTED)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="service_requests")
