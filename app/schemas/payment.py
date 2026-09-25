from datetime import date
from pydantic import BaseModel, Field
from app.utils.enums import PaymentMethod, PaymentStatus


class PaymentCreate(BaseModel):
    amount: float = Field(gt=0)
    payment_method: PaymentMethod
    transaction_id: str = Field(min_length=3)
    payment_date: date


class PaymentResponse(BaseModel):
    id: int
    bill_id: int
    amount: float
    payment_method: PaymentMethod
    transaction_id: str
    payment_date: date
    payment_status: PaymentStatus

    model_config = {"from_attributes": True}
