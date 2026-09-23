"""
Booking model.

Mobile field mapping (camelCase → snake_case):
  id            → id
  customerId    → customer_id       (FK → users.id, RESTRICT)
  workerId      → worker_id         (FK → workers.id, SET NULL — allows unassigned)
  serviceId     → service_id        (FK → service_categories.id, RESTRICT)
  type          → type              (enum: scheduled | emergency)
  status        → status            (enum: pending→…→completed + rejected/cancelled/unassigned)
  scheduledAt   → scheduled_at
  address.text  → address_text
  address.lat   → address_lat
  address.lng   → address_lng
  notes         → notes
  priceEstimate → price_estimate
  paymentMode   → payment_mode
  paymentStatus → payment_status    (enum: pending | paid | cash)
  matchReason   → match_reason
  timeline[]    → timeline          (JSONB array)

Cascade / FK policy:
  - customer_id  → RESTRICT: cannot delete a User who has bookings.
  - worker_id    → SET NULL: worker can be unassigned; booking survives.
  - service_id   → RESTRICT: cannot delete a ServiceCategory with bookings.
"""

from sqlalchemy import Column, String, Float, Text, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
from backend.app.models.enums import BookingStatus, BookingType, PaymentStatus


class Booking(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "bookings"

    # ── Foreign keys ────────────────────────────────────────────────────────
    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    worker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workers.id", ondelete="SET NULL"),
        nullable=True,  # can be null for unassigned emergency bookings
    )
    service_id = Column(
        UUID(as_uuid=True),
        ForeignKey("service_categories.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # ── Type & status ───────────────────────────────────────────────────────
    type = Column(
        Enum(BookingType, name="booking_type", native_enum=True),
        nullable=False,
    )
    status = Column(
        Enum(BookingStatus, name="booking_status", native_enum=True),
        nullable=False,
        default=BookingStatus.PENDING,
    )

    # ── Scheduling ──────────────────────────────────────────────────────────
    scheduled_at = Column(DateTime(timezone=True), nullable=True)

    # ── Address (flattened from mobile's address{} object) ──────────────────
    address_text = Column(String(500), nullable=True)
    address_lat = Column(Float, nullable=True)
    address_lng = Column(Float, nullable=True)

    # ── Details ─────────────────────────────────────────────────────────────
    notes = Column(Text, nullable=True)
    price_estimate = Column(Float, nullable=True)
    payment_mode = Column(String(20), nullable=True)  # "cash", "online", etc.
    payment_status = Column(
        Enum(PaymentStatus, name="payment_status", native_enum=True),
        nullable=False,
        default=PaymentStatus.PENDING,
    )
    match_reason = Column(String(500), nullable=True)  # AI match explanation

    # ── Timeline (JSONB array of {status, timestamp, note}) ─────────────────
    timeline = Column(JSONB, nullable=False, default=[])

    # ── Relationships ────────────────────────────────────────────────────────
    customer = relationship("User", foreign_keys=[customer_id])
    worker = relationship("Worker", foreign_keys=[worker_id])
    service = relationship("ServiceCategory")
    reviews = relationship("Review", back_populates="booking")
    earnings = relationship("Earning", back_populates="booking")

    def __repr__(self):
        return f"<Booking id={self.id} type={self.type} status={self.status}>"
