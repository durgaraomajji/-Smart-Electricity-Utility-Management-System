from fastapi import HTTPException
from app.models.customer import Customer
from app.models.service_request import ServiceRequest
from app.utils.enums import CustomerStatus, ServiceRequestStatus


class ServiceRequestService:
    @staticmethod
    def create(db,data):
        customer=db.get(Customer,data.customer_id)
        if not customer: raise HTTPException(404,"Customer not found")
        if customer.status == CustomerStatus.SUSPENDED.value:
            raise HTTPException(400,"Suspended customers cannot create service requests")
        obj=ServiceRequest(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj
