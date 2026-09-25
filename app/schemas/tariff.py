from datetime import date
from pydantic import BaseModel, Field
from app.utils.enums import ConnectionType


class TariffCreate(BaseModel):
    tariff_name: str
    connection_type: ConnectionType
    minimum_units: float = Field(ge=0)
    maximum_units: float | None = Field(default=None, gt=0)
    rate_per_unit: float = Field(gt=0)
    fixed_charge: float = Field(ge=0)
    effective_from: date
    effective_to: date | None = None
    status: bool = True


class TariffUpdate(BaseModel):
    tariff_name: str | None = None
    rate_per_unit: float | None = Field(default=None, gt=0)
    fixed_charge: float | None = Field(default=None, ge=0)
    effective_to: date | None = None
    status: bool | None = None


class TariffResponse(TariffCreate):
    id: int
    model_config = {"from_attributes": True}
