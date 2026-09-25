from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, Enum as SAEnum, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.utils.enums import ConnectionType


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    tariff_name: Mapped[str] = mapped_column(String(120))
    connection_type: Mapped[str] = mapped_column(SAEnum(ConnectionType), index=True)
    minimum_units: Mapped[float] = mapped_column(Float)
    maximum_units: Mapped[float | None] = mapped_column(Float, nullable=True)
    rate_per_unit: Mapped[float] = mapped_column(Float)
    fixed_charge: Mapped[float] = mapped_column(Float, default=0)
    effective_from: Mapped[date] = mapped_column(Date)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
