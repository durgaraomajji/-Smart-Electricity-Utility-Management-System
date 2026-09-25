from datetime import date
from pydantic import BaseModel, Field
from app.utils.enums import ConnectionType, ConnectionStatus


class ConnectionCreate(BaseModel):
    customer_id: int
    connection_number: str
    connection_type: ConnectionType
    sanctioned_load: float = Field(gt=0)
    tariff_type: str
    connection_date: date
    status: ConnectionStatus = ConnectionStatus.ACTIVE


class ConnectionUpdate(BaseModel):
    connection_type: ConnectionType | None = None
    sanctioned_load: float | None = Field(default=None, gt=0)
    tariff_type: str | None = None
    status: ConnectionStatus | None = None


class ConnectionResponse(ConnectionCreate):
    id: int
    model_config = {"from_attributes": True}
