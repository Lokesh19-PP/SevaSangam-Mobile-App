"""
Shared Python enums — used by both SQLAlchemy models and Pydantic schemas.

Values match the provisional enums in ANTIGRAVITY_MOBILE_CONTEXT.md § 7 exactly.
"""

import enum


# ── User ────────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    WORKER = "worker"
    ADMIN = "admin"


# ── Worker ──────────────────────────────────────────────────────────────────

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class WorkerAvailability(str, enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


class InsuranceStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    NONE = "none"


# ── Certificate ─────────────────────────────────────────────────────────────

class CertificateStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# ── Booking ─────────────────────────────────────────────────────────────────

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    ACCEPTED = "accepted"
    EN_ROUTE = "en_route"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    UNASSIGNED = "unassigned"  # emergency with no taker


class BookingType(str, enum.Enum):
    SCHEDULED = "scheduled"
    EMERGENCY = "emergency"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CASH = "cash"


# ── Complaint ───────────────────────────────────────────────────────────────

class ComplaintStatus(str, enum.Enum):
    OPEN = "open"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    REJECTED = "rejected"


# ── Welfare Program ─────────────────────────────────────────────────────────

class WelfareProgramType(str, enum.Enum):
    INSURANCE = "insurance"
    HEALTH = "health"
    TRAINING = "training"
    OTHER = "other"


class WelfareProgramStatus(str, enum.Enum):
    ACTIVE = "active"
    DRAFT = "draft"
    CLOSED = "closed"

