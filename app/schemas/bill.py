from datetime import date
from pydantic import BaseModel, Field
from app.utils.enums import BillStatus


class BillGenerateRequest(BaseModel):
    connection_id: int
    billing_month: str = Field(pattern=r"^\d{4}-\d{2}$")
    units_consumed: float | None = Field(default=None, ge=0)
    late_fee: float = Field(default=0, ge=0)
    discount: float = Field(default=0, ge=0)
    due_date: date


class BillResponse(BaseModel):
    id: int
    connection_id: int
    billing_month: str
    units_consumed: float
    energy_charge: float
    fixed_charge: float
    tax: float
    late_fee: float
    discount: float
    total_amount: float
    due_date: date
    bill_status: BillStatus

    model_config = {"from_attributes": True}
