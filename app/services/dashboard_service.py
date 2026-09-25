from datetime import date
from sqlalchemy import select, func
from app.models.customer import Customer
from app.models.connection import Connection
from app.models.meter import Meter
from app.models.meter_reading import MeterReading
from app.models.bill import Bill
from app.models.complaint import Complaint
from app.utils.enums import ConnectionStatus, MeterStatus, BillStatus, ComplaintStatus


class DashboardService:
    @staticmethod
    def get(db, billing_month: str | None = None):
        month=billing_month or date.today().strftime("%Y-%m")
        return {
            "total_customers": db.scalar(select(func.count(Customer.id)).where(Customer.is_deleted==False)) or 0,
            "active_connections": db.scalar(select(func.count(Connection.id)).where(Connection.status==ConnectionStatus.ACTIVE.value)) or 0,
            "disconnected_connections": db.scalar(select(func.count(Connection.id)).where(Connection.status==ConnectionStatus.DISCONNECTED.value)) or 0,
            "total_meters": db.scalar(select(func.count(Meter.id))) or 0,
            "faulty_meters": db.scalar(select(func.count(Meter.id)).where(Meter.meter_status==MeterStatus.FAULTY.value)) or 0,
            "monthly_units_consumed": float(db.scalar(select(func.coalesce(func.sum(MeterReading.units_consumed),0)).where(func.substr(MeterReading.reading_date,1,7)==month)) or 0),
            "monthly_revenue": float(db.scalar(select(func.coalesce(func.sum(Bill.total_amount),0)).where(Bill.billing_month==month, Bill.bill_status==BillStatus.PAID.value)) or 0),
            "pending_bills": db.scalar(select(func.count(Bill.id)).where(Bill.bill_status==BillStatus.PENDING.value)) or 0,
            "overdue_bills": db.scalar(select(func.count(Bill.id)).where(Bill.bill_status==BillStatus.OVERDUE.value)) or 0,
            "open_complaints": db.scalar(select(func.count(Complaint.id)).where(Complaint.status.in_([ComplaintStatus.OPEN.value,ComplaintStatus.ASSIGNED.value,ComplaintStatus.IN_PROGRESS.value]))) or 0,
            "resolved_complaints": db.scalar(select(func.count(Complaint.id)).where(Complaint.status==ComplaintStatus.RESOLVED.value)) or 0,
        }
