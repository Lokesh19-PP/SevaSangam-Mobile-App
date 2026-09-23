"""
SQLAlchemy declarative base and shared column mixins.
"""

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
import uuid


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


class TimestampMixin:
    """Adds created_at / updated_at columns to any model that inherits this."""

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    """Adds a UUID primary key column named `id`."""

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
