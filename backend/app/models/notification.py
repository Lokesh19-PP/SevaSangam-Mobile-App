"""
Notification model.

Mobile field mapping (camelCase → snake_case):
  id        → id
  userId    → user_id      (FK → users.id, CASCADE)
  type      → type
  titleKey  → title_key    (i18n key)
  body      → body
  read      → read
  createdAt → created_at   (from TimestampMixin)

Cascade / FK policy:
  - user_id → CASCADE: notifications are deleted when the user is deleted.
"""

from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin


class Notification(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "notifications"

    # ── Foreign key ──────────────────────────────────────────────────────────
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Notification data ────────────────────────────────────────────────────
    type = Column(String(50), nullable=False)     # e.g. "booking_update", "emergency", "verification"
    title_key = Column(String(100), nullable=False)  # i18n key
    body = Column(Text, nullable=True)
    read = Column(Boolean, nullable=False, default=False, index=True)

    # ── Relationships ────────────────────────────────────────────────────────
    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return f"<Notification id={self.id} type={self.type!r} read={self.read}>"
