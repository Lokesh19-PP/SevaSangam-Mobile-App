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
