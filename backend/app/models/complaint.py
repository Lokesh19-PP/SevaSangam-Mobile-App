"""
Complaint model.

Mobile field mapping (camelCase → snake_case):
  id             → id
  raisedBy       → raised_by       (FK → users.id, SET NULL)
  bookingId      → booking_id      (FK → bookings.id, SET NULL, nullable)
  workerId       → worker_id       (FK → workers.id, SET NULL, nullable)
  category       → category
  description    → description
  status         → status          (enum: open | in_review | resolved | rejected)
  resolutionNote → resolution_note
  createdAt      → created_at      (from TimestampMixin)

Cascade / FK policy:
  - raised_by  → SET NULL: complaint survives if user is deleted (audit trail).
  - booking_id → SET NULL: complaint survives if booking is removed.
  - worker_id  → SET NULL: complaint survives if worker is removed.
"""

from sqlalchemy import Column, String, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
from backend.app.models.enums import ComplaintStatus


class Complaint(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "complaints"

    # ── Foreign keys ────────────────────────────────────────────────────────
    raised_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    booking_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="SET NULL"),
        nullable=True,
    )
    worker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workers.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ── Complaint data ──────────────────────────────────────────────────────
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(
        Enum(ComplaintStatus, name="complaint_status", native_enum=True),
        nullable=False,
        default=ComplaintStatus.OPEN,
    )
    resolution_note = Column(Text, nullable=True)

    # ── Relationships ────────────────────────────────────────────────────────
    raiser = relationship("User", foreign_keys=[raised_by])
    booking = relationship("Booking", foreign_keys=[booking_id])
    worker = relationship("Worker", foreign_keys=[worker_id])

    def __repr__(self):
        return f"<Complaint id={self.id} status={self.status}>"
