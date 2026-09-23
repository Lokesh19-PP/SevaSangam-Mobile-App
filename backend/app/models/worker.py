"""
Worker model.

Mobile field mapping (camelCase → snake_case):
  id                → id
  userId            → user_id             (FK → users.id)
  cooperativeId     → cooperative_id      (FK → cooperatives.id)
  skills[]          → skills              (ARRAY of String)
  experienceYears   → experience_years
  rating            → rating
  ratingCount       → rating_count
  verificationStatus → verification_status (enum: pending | verified | rejected | suspended)
  availability      → availability        (enum: available | busy | offline)
  location{lat,lng} → location            (PostGIS Geography(Point, 4326))
  serviceRadiusKm   → service_radius_km
  workloadThisWeek  → workload_this_week
  insurance.status  → insurance_status    (enum: active | expired | none)
  insurance.coverage → insurance_coverage
  insurance.validTill → insurance_valid_till
"""

from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey, Date
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
from backend.app.models.enums import (
    VerificationStatus,
    WorkerAvailability,
    InsuranceStatus,
)


class Worker(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workers"

    # ── Foreign keys ────────────────────────────────────────────────────────
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    cooperative_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cooperatives.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ── Profile ─────────────────────────────────────────────────────────────
    skills = Column(ARRAY(String), nullable=False, default=[])
    experience_years = Column(Integer, nullable=False, default=0)

    # ── Ratings ─────────────────────────────────────────────────────────────
    rating = Column(Float, nullable=False, default=0.0, index=True)
    rating_count = Column(Integer, nullable=False, default=0)

    # ── Status ──────────────────────────────────────────────────────────────
    verification_status = Column(
        Enum(VerificationStatus, name="verification_status", native_enum=True),
        nullable=False,
        default=VerificationStatus.PENDING,
        index=True,
    )
    availability = Column(
        Enum(WorkerAvailability, name="worker_availability", native_enum=True),
        nullable=False,
        default=WorkerAvailability.OFFLINE,
        index=True,
    )

    # ── Geo ──────────────────────────────────────────────────────────────────
    # PostGIS Geography point (SRID 4326 = WGS 84 lat/lng).
    # Stores as POINT(longitude latitude) — note the order.
    location = Column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=True,
    )
    service_radius_km = Column(Float, nullable=False, default=10.0)

    # ── Workload ─────────────────────────────────────────────────────────────
    workload_this_week = Column(Integer, nullable=False, default=0)

    # ── Insurance (flattened from mobile's insurance{} object) ───────────────
    insurance_status = Column(
        Enum(InsuranceStatus, name="insurance_status", native_enum=True),
        nullable=False,
        default=InsuranceStatus.NONE,
    )
    insurance_coverage = Column(String(255), nullable=True)
    insurance_valid_till = Column(Date, nullable=True)

    # ── Relationships ────────────────────────────────────────────────────────
    user = relationship("User", back_populates="worker_profile")
    cooperative = relationship("Cooperative", back_populates="workers")
    certificates = relationship("Certificate", back_populates="worker")

    def __repr__(self):
        return f"<Worker id={self.id} user_id={self.user_id} status={self.verification_status}>"
