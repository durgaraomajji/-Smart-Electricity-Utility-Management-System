from pydantic import BaseModel, EmailStr, Field
from app.utils.enums import CustomerStatus


class CustomerCreate(BaseModel):
    customer_number: str = Field(min_length=2, max_length=50)
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: str
    address: str
    city: str
    status: CustomerStatus = CustomerStatus.ACTIVE
    user_id: int | None = None


class CustomerUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    status: CustomerStatus | None = None


class CustomerResponse(CustomerCreate):
    id: int
    is_deleted: bool

    model_config = {"from_attributes": True}
