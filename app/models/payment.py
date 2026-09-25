from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SAEnum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.utils.enums import PaymentMethod, PaymentStatus


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    bill_id: Mapped[int] = mapped_column(ForeignKey("bills.id"), index=True)
    amount: Mapped[float] = mapped_column(Float)
    payment_method: Mapped[str] = mapped_column(SAEnum(PaymentMethod))
    transaction_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    payment_date: Mapped[date] = mapped_column(Date)
    payment_status: Mapped[str] = mapped_column(SAEnum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    bill = relationship("Bill", back_populates="payments")
