"""
Pydantic schemas for Earning.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date, datetime

from backend.app.models.enums import PaymentStatus


# ── Base ────────────────────────────────────────────────────────────────────

class EarningBase(BaseModel):
    amount: float = Field(..., gt=0)
    date: date


# ── Create ──────────────────────────────────────────────────────────────────

class EarningCreate(EarningBase):
    worker_id: UUID = Field(..., alias="workerId")
    booking_id: UUID = Field(..., alias="bookingId")
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING, alias="paymentStatus")

    model_config = {"populate_by_name": True}


# ── Update ──────────────────────────────────────────────────────────────────

class EarningUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    payment_status: Optional[PaymentStatus] = Field(default=None, alias="paymentStatus")

    model_config = {"populate_by_name": True}


# ── Response ────────────────────────────────────────────────────────────────

class EarningResponse(EarningBase):
    id: UUID
    worker_id: UUID = Field(..., alias="workerId")
    booking_id: UUID = Field(..., alias="bookingId")
    payment_status: PaymentStatus = Field(..., alias="paymentStatus")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
