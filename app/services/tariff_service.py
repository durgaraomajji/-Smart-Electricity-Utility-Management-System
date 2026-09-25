from sqlalchemy import select
from fastapi import HTTPException
from app.models.tariff import Tariff


class TariffService:
    @staticmethod
    def create(db,data):
        if data.maximum_units is not None and data.maximum_units < data.minimum_units:
            raise HTTPException(400,"Maximum units must be >= minimum units")
        obj=Tariff(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

    @staticmethod
    def get_active(db, connection_type, units, bill_date):
        q=select(Tariff).where(
            Tariff.connection_type==connection_type,
            Tariff.minimum_units<=units,
            Tariff.status==True,
            Tariff.effective_from<=bill_date,
        )
        tariffs=db.scalars(q.order_by(Tariff.minimum_units.desc())).all()
        for t in tariffs:
            if t.maximum_units is None or units <= t.maximum_units:
                return t
        raise HTTPException(400,"No applicable tariff found")
