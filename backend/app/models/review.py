"""
Review model.

Mobile field mapping (camelCase → snake_case):
  id         → id
  bookingId  → booking_id    (FK → bookings.id, CASCADE)
  customerId → customer_id   (FK → users.id, RESTRICT)
  workerId   → worker_id     (FK → workers.id, RESTRICT)
  stars      → stars
  comment    → comment
  tags[]     → tags          (ARRAY of String)
  createdAt  → created_at    (from TimestampMixin)

Cascade / FK policy:
  - booking_id  → CASCADE: deleting a booking removes its review.
  - customer_id → RESTRICT: cannot delete user who left reviews.
  - worker_id   → RESTRICT: cannot delete worker who has reviews.
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin


class Review(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "reviews"

    # ── Foreign keys ────────────────────────────────────────────────────────
    booking_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # one review per booking
    )
    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    worker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # ── Review data ─────────────────────────────────────────────────────────
    stars = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    tags = Column(ARRAY(String), nullable=False, default=[])

    # ── Constraints ─────────────────────────────────────────────────────────
    __table_args__ = (
        CheckConstraint("stars >= 1 AND stars <= 5", name="ck_reviews_stars_range"),
    )

    # ── Relationships ────────────────────────────────────────────────────────
    booking = relationship("Booking", back_populates="reviews")
    customer = relationship("User", foreign_keys=[customer_id])
    worker = relationship("Worker", foreign_keys=[worker_id])

    def __repr__(self):
        return f"<Review id={self.id} stars={self.stars}>"
