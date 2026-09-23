"""
Pydantic schemas for Cooperative.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


# ── Base ────────────────────────────────────────────────────────────────────

class CooperativeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    region: str = Field(..., min_length=1, max_length=255)
    member_count: int = Field(default=0, alias="memberCount", ge=0)
    verified: bool = False


# ── Create ──────────────────────────────────────────────────────────────────

class CooperativeCreate(CooperativeBase):
    pass


# ── Update ──────────────────────────────────────────────────────────────────

class CooperativeUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    region: Optional[str] = Field(default=None, min_length=1, max_length=255)
    member_count: Optional[int] = Field(default=None, alias="memberCount", ge=0)
    verified: Optional[bool] = None


# ── Response ────────────────────────────────────────────────────────────────

class CooperativeResponse(CooperativeBase):
    id: UUID
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
