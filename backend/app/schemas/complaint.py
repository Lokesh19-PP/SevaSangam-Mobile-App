"""
Pydantic schemas for Complaint.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from backend.app.models.enums import ComplaintStatus


# ── Base ────────────────────────────────────────────────────────────────────

class ComplaintBase(BaseModel):
    category: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)


# ── Create ──────────────────────────────────────────────────────────────────

class ComplaintCreate(ComplaintBase):
    raised_by: UUID = Field(..., alias="raisedBy")
    booking_id: Optional[UUID] = Field(default=None, alias="bookingId")
    worker_id: Optional[UUID] = Field(default=None, alias="workerId")

    model_config = {"populate_by_name": True}


# ── Update ──────────────────────────────────────────────────────────────────

class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None
    resolution_note: Optional[str] = Field(default=None, alias="resolutionNote")

    model_config = {"populate_by_name": True}


# ── Response ────────────────────────────────────────────────────────────────

class ComplaintResponse(ComplaintBase):
    id: UUID
    raised_by: Optional[UUID] = Field(default=None, alias="raisedBy")
    booking_id: Optional[UUID] = Field(default=None, alias="bookingId")
    worker_id: Optional[UUID] = Field(default=None, alias="workerId")
    status: ComplaintStatus
    resolution_note: Optional[str] = Field(default=None, alias="resolutionNote")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
