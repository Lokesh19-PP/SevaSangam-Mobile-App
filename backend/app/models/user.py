"""
User model.

Mobile field mapping (camelCase → snake_case):
  id          → id
  role        → role          (enum: customer | worker | admin)
  name        → name
  phone       → phone
  language    → language
  avatar      → avatar
"""

from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from backend.app.models.base import Base, UUIDPrimaryKeyMixin, TimestampMixin
from backend.app.models.enums import UserRole


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    role = Column(
        Enum(UserRole, name="user_role", native_enum=True),
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False, unique=True)  # Indian +91 format
    language = Column(String(5), nullable=False, default="en")  # en | hi | mr
    avatar = Column(String(512), nullable=True)  # URL to profile image

    # Relationships (back-populated from Worker side)
    worker_profile = relationship("Worker", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User id={self.id} name={self.name!r} role={self.role}>"
