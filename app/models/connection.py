from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SAEnum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.utils.enums import ConnectionType, ConnectionStatus


class Connection(Base):
    __tablename__ = "connections"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    connection_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    connection_type: Mapped[str] = mapped_column(SAEnum(ConnectionType))
    sanctioned_load: Mapped[float] = mapped_column(Float)
    tariff_type: Mapped[str] = mapped_column(String(100))
    connection_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(SAEnum(ConnectionStatus), default=ConnectionStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="connections")
    meters = relationship("Meter", back_populates="connection")
    bills = relationship("Bill", back_populates="connection")
    complaints = relationship("Complaint", back_populates="connection")
