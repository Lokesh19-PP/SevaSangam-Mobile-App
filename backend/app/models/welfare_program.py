"""
WelfareProgram model.

Mobile field mapping (camelCase → snake_case):
  id            → id
  title         → title
  description   → description
  type          → type            (enum: insurance | health | training | other)
  eligibility   → eligibility
  enrolledCount → enrolled_count
  status        → status          (enum: active | draft | closed)
"""

from sqlalchemy import Column, String, Integer, Text, Enum

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
from backend.app.models.enums import WelfareProgramType, WelfareProgramStatus


class WelfareProgram(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "welfare_programs"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(
        Enum(WelfareProgramType, name="welfare_program_type", native_enum=True),
        nullable=False,
        index=True,
    )
    eligibility = Column(String(500), nullable=True)
    enrolled_count = Column(Integer, nullable=False, default=0)
    status = Column(
        Enum(WelfareProgramStatus, name="welfare_program_status", native_enum=True),
        nullable=False,
        default=WelfareProgramStatus.DRAFT,
        index=True,
    )

    def __repr__(self):
        return f"<WelfareProgram id={self.id} title={self.title!r}>"
