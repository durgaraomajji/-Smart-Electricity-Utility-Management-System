from pydantic import BaseModel


class MonthlyConsumptionResponse(BaseModel):
    month: str
    units_consumed: float
    bill_amount: float


class AnalyticsSummary(BaseModel):
    total_units: float
    average_monthly_units: float
