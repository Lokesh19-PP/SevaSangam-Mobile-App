"""
Certificate model.

Mobile field mapping (camelCase → snake_case):
  id         → id
  workerId   → worker_id     (FK → workers.id)
  type       → type
  imageUrl   → image_url
  ocr.text   → ocr_text
  ocr.confidence → ocr_confidence
  status     → status        (enum: pending | approved | rejected)
  reviewNote → review_note
"""

from sqlalchemy import Column, String, Float, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
from backend.app.models.enums import CertificateStatus


class Certificate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "certificates"

    # ── Foreign key ──────────────────────────────────────────────────────────
    worker_id = Column(
        UUID(as_uuid=True),
        ForeignKey("workers.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── Certificate data ─────────────────────────────────────────────────────
    type = Column(String(100), nullable=False)  # e.g. "electrician_license", "safety_training"
    image_url = Column(String(512), nullable=True)

    # ── OCR results (flattened from mobile's ocr{} object) ───────────────────
    ocr_text = Column(Text, nullable=True)
    ocr_confidence = Column(Float, nullable=True)

    # ── Review ───────────────────────────────────────────────────────────────
    status = Column(
        Enum(CertificateStatus, name="certificate_status", native_enum=True),
        nullable=False,
        default=CertificateStatus.PENDING,
    )
    review_note = Column(Text, nullable=True)

    # ── Relationships ────────────────────────────────────────────────────────
    worker = relationship("Worker", back_populates="certificates")

    def __repr__(self):
        return f"<Certificate id={self.id} type={self.type!r} status={self.status}>"
