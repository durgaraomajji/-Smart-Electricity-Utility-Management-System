from app.utils.enums import UserRole

ADMIN_ROLES = (UserRole.SUPER_ADMIN.value,)
BILLING_ROLES = (UserRole.SUPER_ADMIN.value, UserRole.BILLING_OFFICER.value)
TECHNICIAN_ROLES = (UserRole.SUPER_ADMIN.value, UserRole.FIELD_TECHNICIAN.value)
SERVICE_ROLES = (
    UserRole.SUPER_ADMIN.value,
    UserRole.CUSTOMER_SERVICE_AGENT.value,
)
