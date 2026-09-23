"""
Cooperative model.

Mobile field mapping (camelCase → snake_case):
  id          → id
  name        → name
  region      → region
  memberCount → member_count
  verified    → verified
"""

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin


class Cooperative(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "cooperatives"

    name = Column(String(255), nullable=False)
    region = Column(String(255), nullable=False)
    member_count = Column(Integer, nullable=False, default=0)
    verified = Column(Boolean, nullable=False, default=False)

    # Relationships
    workers = relationship("Worker", back_populates="cooperative")

    def __repr__(self):
        return f"<Cooperative id={self.id} name={self.name!r}>"
