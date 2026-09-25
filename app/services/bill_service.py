from sqlalchemy import select, func
from fastapi import HTTPException
from app.models.bill import Bill
from app.models.connection import Connection
from app.models.meter_reading import MeterReading
from app.services.tariff_service import TariffService
from app.config import settings
from app.utils.enums import ConnectionStatus, BillStatus


class BillService:
    @staticmethod
    def generate(db, data):
        connection=db.get(Connection,data.connection_id)
        if not connection: raise HTTPException(404,"Connection not found")
        if connection.status != ConnectionStatus.ACTIVE.value:
            raise HTTPException(400,"Disconnected or inactive connection cannot generate regular bills")
        duplicate=db.scalar(select(Bill).where(Bill.connection_id==data.connection_id, Bill.billing_month==data.billing_month))
        if duplicate: raise HTTPException(400,"Bill already exists for this connection and month")
        units=data.units_consumed
        if units is None:
            month=data.billing_month
            units=db.scalar(select(func.coalesce(func.sum(MeterReading.units_consumed),0)).join(MeterReading.meter).where(
                MeterReading.reading_date.like(f"{month}%")
            )) or 0
        from datetime import date
        bill_date=date.fromisoformat(data.billing_month+"-01")
        tariff=TariffService.get_active(db, connection.connection_type, units, bill_date)
        energy=units*tariff.rate_per_unit
        fixed=tariff.fixed_charge
        tax=(energy+fixed)*settings.TAX_RATE
        total=energy+fixed+tax+data.late_fee-data.discount
        if total <= 0: raise HTTPException(400,"Bill amount must be greater than 0")
        obj=Bill(
            connection_id=data.connection_id,billing_month=data.billing_month,
            units_consumed=units,energy_charge=energy,fixed_charge=fixed,tax=tax,
            late_fee=data.late_fee,discount=data.discount,total_amount=total,
            due_date=data.due_date,bill_status=BillStatus.PENDING.value
        )
        db.add(obj); db.commit(); db.refresh(obj); return obj
