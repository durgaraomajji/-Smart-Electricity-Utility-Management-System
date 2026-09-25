from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def create_audit_log(db: Session, user_id: int | None, action: str, entity: str, entity_id: int | None):
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
    )
    db.add(log)
    db.flush()
    return log
