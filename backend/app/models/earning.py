"""
Earning model.

Mobile field mapping (camelCase → snake_case):
  id            → id
  workerId      → worker_id       (FK → workers.id, RESTRICT)
  bookingId     → booking_id      (FK → bookings.id, RESTRICT)
  amount        → amount
  paymentStatus → payment_status  (enum: pending | paid | cash)
  date          → date

Cascade / FK policy:
  - worker_id  → RESTRICT: cannot delete a worker with earnings records.
  - booking_id → RESTRICT: cannot delete a booking with earnings records.
"""

from sqlalchemy import Column, Float, Date, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
from backend.app.models.enums import PaymentStatus


class Earning(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "earnings"

    # ── Foreign keys ────────────────────────────────────────────────────────
    worker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workers.id", ondelete="RESTRICT"),
        nullable=False,
    )
    booking_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # ── Earning data ────────────────────────────────────────────────────────
    amount = Column(Float, nullable=False)
    payment_status = Column(
        Enum(PaymentStatus, name="payment_status", native_enum=True, create_constraint=False),
        nullable=False,
        default=PaymentStatus.PENDING,
    )
    date = Column(Date, nullable=False)

    # ── Relationships ────────────────────────────────────────────────────────
    worker = relationship("Worker", foreign_keys=[worker_id])
    booking = relationship("Booking", back_populates="earnings")

    def __repr__(self):
        return f"<Earning id={self.id} amount={self.amount}>"
