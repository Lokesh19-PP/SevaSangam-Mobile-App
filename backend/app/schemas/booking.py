"""
Pydantic schemas for Booking.

The DB flattens `address` to address_text/lat/lng.
The API schema nests it back as address: { text, lat, lng }.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime

from backend.app.models.enums import BookingStatus, BookingType, PaymentStatus


# ── Nested sub-schema ───────────────────────────────────────────────────────

class AddressSchema(BaseModel):
    text: Optional[str] = None
    lat: Optional[float] = Field(default=None, ge=-90, le=90)
    lng: Optional[float] = Field(default=None, ge=-180, le=180)


class TimelineEntry(BaseModel):
    status: str
    timestamp: datetime
    note: Optional[str] = None


# ── Base ────────────────────────────────────────────────────────────────────

class BookingBase(BaseModel):
    type: BookingType
    notes: Optional[str] = None
    price_estimate: Optional[float] = Field(default=None, alias="priceEstimate", ge=0)
    payment_mode: Optional[str] = Field(default=None, alias="paymentMode")

    model_config = {"populate_by_name": True}


# ── Create ──────────────────────────────────────────────────────────────────

class BookingCreate(BookingBase):
    customer_id: UUID = Field(..., alias="customerId")
    worker_id: Optional[UUID] = Field(default=None, alias="workerId")
    service_id: UUID = Field(..., alias="serviceId")
    scheduled_at: Optional[datetime] = Field(default=None, alias="scheduledAt")
    address: Optional[AddressSchema] = None


# ── Update ──────────────────────────────────────────────────────────────────

class BookingUpdate(BaseModel):
    worker_id: Optional[UUID] = Field(default=None, alias="workerId")
    status: Optional[BookingStatus] = None
    scheduled_at: Optional[datetime] = Field(default=None, alias="scheduledAt")
    address: Optional[AddressSchema] = None
    notes: Optional[str] = None
    price_estimate: Optional[float] = Field(default=None, alias="priceEstimate", ge=0)
    payment_mode: Optional[str] = Field(default=None, alias="paymentMode")
    payment_status: Optional[PaymentStatus] = Field(default=None, alias="paymentStatus")
    match_reason: Optional[str] = Field(default=None, alias="matchReason")

    model_config = {"populate_by_name": True}


# ── Response ────────────────────────────────────────────────────────────────

class BookingResponse(BookingBase):
    id: UUID
    customer_id: UUID = Field(..., alias="customerId")
    worker_id: Optional[UUID] = Field(default=None, alias="workerId")
    service_id: UUID = Field(..., alias="serviceId")
    status: BookingStatus
    scheduled_at: Optional[datetime] = Field(default=None, alias="scheduledAt")
    address: Optional[AddressSchema] = None
    payment_status: PaymentStatus = Field(..., alias="paymentStatus")
    match_reason: Optional[str] = Field(default=None, alias="matchReason")
    timeline: List[TimelineEntry] = []
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
