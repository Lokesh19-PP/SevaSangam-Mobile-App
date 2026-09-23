"""
Pydantic schemas for Review.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# ── Base ────────────────────────────────────────────────────────────────────

class ReviewBase(BaseModel):
    stars: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    tags: List[str] = []


# ── Create ──────────────────────────────────────────────────────────────────

class ReviewCreate(ReviewBase):
    booking_id: UUID = Field(..., alias="bookingId")
    customer_id: UUID = Field(..., alias="customerId")
    worker_id: UUID = Field(..., alias="workerId")

    model_config = {"populate_by_name": True}


# ── Update ──────────────────────────────────────────────────────────────────

class ReviewUpdate(BaseModel):
    stars: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None
    tags: Optional[List[str]] = None


# ── Response ────────────────────────────────────────────────────────────────

class ReviewResponse(ReviewBase):
    id: UUID
    booking_id: UUID = Field(..., alias="bookingId")
    customer_id: UUID = Field(..., alias="customerId")
    worker_id: UUID = Field(..., alias="workerId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
