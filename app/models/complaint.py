from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.utils.enums import ComplaintType, Priority, ComplaintStatus


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    connection_id: Mapped[int | None] = mapped_column(ForeignKey("connections.id"), nullable=True)
    complaint_type: Mapped[str] = mapped_column(SAEnum(ComplaintType))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(SAEnum(Priority), index=True)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("technicians.id"), nullable=True)
    status: Mapped[str] = mapped_column(SAEnum(ComplaintStatus), default=ComplaintStatus.OPEN, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    customer = relationship("Customer", back_populates="complaints")
    connection = relationship("Connection", back_populates="complaints")
    technician = relationship("Technician", back_populates="complaints")
    history = relationship("ComplaintHistory", back_populates="complaint", cascade="all, delete-orphan")
