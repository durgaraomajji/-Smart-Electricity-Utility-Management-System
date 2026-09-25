from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    BILLING_OFFICER = "billing_officer"
    FIELD_TECHNICIAN = "field_technician"
    CUSTOMER_SERVICE_AGENT = "customer_service_agent"
    CUSTOMER = "customer"


class CustomerStatus(str, Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    CLOSED = "Closed"


class ConnectionType(str, Enum):
    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"
    INDUSTRIAL = "Industrial"


class ConnectionStatus(str, Enum):
    ACTIVE = "Active"
    DISCONNECTED = "Disconnected"
    SUSPENDED = "Suspended"


class MeterStatus(str, Enum):
    ACTIVE = "Active"
    FAULTY = "Faulty"
    REMOVED = "Removed"


class ReadingSource(str, Enum):
    MANUAL = "Manual"
    SMART_METER = "Smart Meter"
    FIELD_TECHNICIAN = "Field Technician"


class BillStatus(str, Enum):
    GENERATED = "Generated"
    PENDING = "Pending"
    PAID = "Paid"
    OVERDUE = "Overdue"
    CANCELLED = "Cancelled"


class PaymentMethod(str, Enum):
    UPI = "UPI"
    CARD = "Card"
    NET_BANKING = "Net Banking"
    WALLET = "Wallet"


class PaymentStatus(str, Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class ComplaintType(str, Enum):
    POWER_FAILURE = "Power Failure"
    VOLTAGE_ISSUE = "Voltage Issue"
    METER_ISSUE = "Meter Issue"
    BILLING_ISSUE = "Billing Issue"
    CONNECTION_ISSUE = "Connection Issue"
    OTHER = "Other"


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    EMERGENCY = "Emergency"


class ComplaintStatus(str, Enum):
    OPEN = "Open"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class AvailabilityStatus(str, Enum):
    AVAILABLE = "Available"
    BUSY = "Busy"
    UNAVAILABLE = "Unavailable"


class ServiceRequestType(str, Enum):
    NEW_CONNECTION = "New Connection"
    LOAD_CHANGE = "Load Change"
    METER_REPLACEMENT = "Meter Replacement"
    NAME_CHANGE = "Name Change"
    ADDRESS_CHANGE = "Address Change"
    DISCONNECTION = "Disconnection"
    RECONNECTION = "Reconnection"


class ServiceRequestStatus(str, Enum):
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    COMPLETED = "Completed"
