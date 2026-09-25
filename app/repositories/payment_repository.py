from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, obj_id: int):
        return self.db.get(Payment, obj_id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.scalars(select(Payment).offset(skip).limit(limit)).all()

    def add(self, obj):
        self.db.add(obj)
        self.db.flush()
        return obj

    def delete(self, obj):
        self.db.delete(obj)
        self.db.flush()
