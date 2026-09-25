from sqlalchemy import select, func
from app.models.meter_reading import MeterReading
from app.models.meter import Meter
from app.models.connection import Connection
from app.models.bill import Bill


class AnalyticsService:
    @staticmethod
    def monthly(db, connection_id):
        rows=db.execute(
            select(
                func.substr(MeterReading.reading_date,1,7).label("month"),
                func.sum(MeterReading.units_consumed).label("units")
            )
            .join(Meter, Meter.id==MeterReading.meter_id)
            .where(Meter.connection_id==connection_id)
            .group_by(func.substr(MeterReading.reading_date,1,7))
            .order_by(func.substr(MeterReading.reading_date,1,7))
        ).all()
        bills={r[0]:r[1] for r in db.execute(select(Bill.billing_month, func.sum(Bill.total_amount)).where(Bill.connection_id==connection_id).group_by(Bill.billing_month)).all()}
        return [{"month":r[0],"units_consumed":float(r[1] or 0),"bill_amount":float(bills.get(r[0],0) or 0)} for r in rows]
