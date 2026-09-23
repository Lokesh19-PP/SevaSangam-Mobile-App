"""
Pydantic schemas for WelfareProgram.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from backend.app.models.enums import WelfareProgramType, WelfareProgramStatus


# ── Base ────────────────────────────────────────────────────────────────────

class WelfareProgramBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    type: WelfareProgramType
    eligibility: Optional[str] = None


# ── Create ──────────────────────────────────────────────────────────────────

class WelfareProgramCreate(WelfareProgramBase):
    status: WelfareProgramStatus = WelfareProgramStatus.DRAFT


# ── Update ──────────────────────────────────────────────────────────────────

class WelfareProgramUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    type: Optional[WelfareProgramType] = None
    eligibility: Optional[str] = None
    enrolled_count: Optional[int] = Field(default=None, alias="enrolledCount", ge=0)
    status: Optional[WelfareProgramStatus] = None

    model_config = {"populate_by_name": True}


# ── Response ────────────────────────────────────────────────────────────────

class WelfareProgramResponse(WelfareProgramBase):
    id: UUID
    enrolled_count: int = Field(default=0, alias="enrolledCount")
    status: WelfareProgramStatus
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
