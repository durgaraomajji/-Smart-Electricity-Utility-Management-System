from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SAEnum, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.utils.enums import BillStatus


class Bill(Base):
    __tablename__ = "bills"
    __table_args__ = (
        UniqueConstraint("connection_id", "billing_month", name="uq_bill_connection_month"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    connection_id: Mapped[int] = mapped_column(ForeignKey("connections.id"), index=True)
    billing_month: Mapped[str] = mapped_column(String(7), index=True)
    units_consumed: Mapped[float] = mapped_column(Float)
    energy_charge: Mapped[float] = mapped_column(Float)
    fixed_charge: Mapped[float] = mapped_column(Float)
    tax: Mapped[float] = mapped_column(Float)
    late_fee: Mapped[float] = mapped_column(Float, default=0)
    discount: Mapped[float] = mapped_column(Float, default=0)
    total_amount: Mapped[float] = mapped_column(Float)
    due_date: Mapped[date] = mapped_column(Date)
    bill_status: Mapped[str] = mapped_column(SAEnum(BillStatus), default=BillStatus.GENERATED, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    connection = relationship("Connection", back_populates="bills")
    payments = relationship("Payment", back_populates="bill")
