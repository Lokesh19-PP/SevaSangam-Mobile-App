"""
Pydantic schemas for Certificate.

DB flattens `ocr` to ocr_text + ocr_confidence.
The API schema nests them back as ocr: { text, confidence }.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from backend.app.models.enums import CertificateStatus


# ── Nested sub-schema ───────────────────────────────────────────────────────

class OcrSchema(BaseModel):
    text: Optional[str] = None
    confidence: Optional[float] = None


# ── Base ────────────────────────────────────────────────────────────────────

class CertificateBase(BaseModel):
    type: str = Field(..., min_length=1, max_length=100)
    image_url: Optional[str] = Field(default=None, alias="imageUrl")

    model_config = {"populate_by_name": True}


# ── Create ──────────────────────────────────────────────────────────────────

class CertificateCreate(CertificateBase):
    worker_id: UUID = Field(..., alias="workerId")


# ── Update ──────────────────────────────────────────────────────────────────

class CertificateUpdate(BaseModel):
    type: Optional[str] = Field(default=None, min_length=1, max_length=100)
    image_url: Optional[str] = Field(default=None, alias="imageUrl")
    status: Optional[CertificateStatus] = None
    review_note: Optional[str] = Field(default=None, alias="reviewNote")
    ocr: Optional[OcrSchema] = None

    model_config = {"populate_by_name": True}


# ── Response ────────────────────────────────────────────────────────────────

class CertificateResponse(CertificateBase):
    id: UUID
    worker_id: UUID = Field(..., alias="workerId")
    ocr: OcrSchema
    status: CertificateStatus
    review_note: Optional[str] = Field(default=None, alias="reviewNote")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
