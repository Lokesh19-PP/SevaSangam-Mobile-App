"""
ServiceCategory model.

Mobile field mapping (camelCase → snake_case):
  id              → id
  key             → key
  name            → name            (i18n key, e.g. "services.electrician")
  icon            → icon
  baseVisitCharge → base_visit_charge
"""

from sqlalchemy import Column, String, Float

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin


class ServiceCategory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "service_categories"

    key = Column(String(50), nullable=False, unique=True)   # e.g. "electrician"
    name = Column(String(100), nullable=False)               # i18n key
    icon = Column(String(100), nullable=True)                # icon name / URL
    base_visit_charge = Column(Float, nullable=False, default=0.0)  # ₹

    def __repr__(self):
        return f"<ServiceCategory id={self.id} key={self.key!r}>"
