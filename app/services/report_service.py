from sqlalchemy import select, func
from app.models.bill import Bill


class ReportService:
    @staticmethod
    def monthly_revenue(db, month: str):
        total=db.scalar(select(func.coalesce(func.sum(Bill.total_amount),0)).where(Bill.billing_month==month)) or 0
        return {"billing_month": month, "revenue": float(total)}
