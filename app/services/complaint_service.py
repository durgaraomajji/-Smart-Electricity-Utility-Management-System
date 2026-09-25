from datetime import datetime
from sqlalchemy import select
from fastapi import HTTPException
from app.models.complaint import Complaint
from app.models.complaint_history import ComplaintHistory
from app.models.technician import Technician
from app.utils.enums import AvailabilityStatus, ComplaintStatus, Priority


class ComplaintService:
    @staticmethod
    def create(db,data):
        priority=data.priority.value
        if priority == Priority.EMERGENCY.value: priority=Priority.EMERGENCY.value
        obj=Complaint(**data.model_dump()); obj.priority=priority.value if hasattr(priority,"value") else priority
        db.add(obj); db.commit(); db.refresh(obj); return obj

    @staticmethod
    def assign(db, complaint_id, technician_id):
        complaint=db.get(Complaint,complaint_id)
        tech=db.get(Technician,technician_id)
        if not complaint: raise HTTPException(404,"Complaint not found")
        if not tech: raise HTTPException(404,"Technician not found")
        if tech.availability_status != AvailabilityStatus.AVAILABLE.value:
            raise HTTPException(400,"Technician is not available")
        old=complaint.status
        complaint.assigned_to=tech.id
        complaint.status=ComplaintStatus.ASSIGNED.value
        tech.availability_status=AvailabilityStatus.BUSY.value
        db.add(ComplaintHistory(complaint_id=complaint.id,old_status=old,new_status=complaint.status,remarks="Technician assigned"))
        db.commit(); db.refresh(complaint); return complaint

    @staticmethod
    def status(db, complaint_id, new_status, user_id, remarks=None):
        complaint=db.get(Complaint,complaint_id)
        if not complaint: raise HTTPException(404,"Complaint not found")
        old=complaint.status; complaint.status=new_status.value
        if new_status.value == ComplaintStatus.RESOLVED.value: complaint.resolved_at=datetime.utcnow()
        db.add(ComplaintHistory(complaint_id=complaint.id,changed_by=user_id,old_status=old,new_status=complaint.status,remarks=remarks))
        db.commit(); db.refresh(complaint); return complaint
