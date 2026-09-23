"""
Pydantic schemas for Worker.

The DB flattens `location` to a PostGIS point and `insurance` to three columns.
The API schemas nest them back to match the mobile contract:
  location:  { lat, lng }
  insurance: { status, coverage, validTill }
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime

from backend.app.models.enums import (
    VerificationStatus,
    WorkerAvailability,
    InsuranceStatus,
)


# ── Nested sub-schemas (match mobile's object shapes) ───────────────────────

class LocationSchema(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class InsuranceSchema(BaseModel):
    status: InsuranceStatus = InsuranceStatus.NONE
    coverage: Optional[str] = None
    valid_till: Optional[date] = Field(default=None, alias="validTill")

    model_config = {"populate_by_name": True}


# ── Base ────────────────────────────────────────────────────────────────────

class WorkerBase(BaseModel):
    skills: List[str] = []
    experience_years: int = Field(default=0, alias="experienceYears", ge=0)
    service_radius_km: float = Field(default=10.0, alias="serviceRadiusKm", ge=0)


# ── Create ──────────────────────────────────────────────────────────────────

class WorkerCreate(WorkerBase):
    user_id: UUID = Field(..., alias="userId")
    cooperative_id: Optional[UUID] = Field(default=None, alias="cooperativeId")
    location: Optional[LocationSchema] = None
    insurance: Optional[InsuranceSchema] = None

    model_config = {"populate_by_name": True}


# ── Update ──────────────────────────────────────────────────────────────────

class WorkerUpdate(BaseModel):
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = Field(default=None, alias="experienceYears", ge=0)
    service_radius_km: Optional[float] = Field(default=None, alias="serviceRadiusKm", ge=0)
    cooperative_id: Optional[UUID] = Field(default=None, alias="cooperativeId")
    location: Optional[LocationSchema] = None
    verification_status: Optional[VerificationStatus] = Field(default=None, alias="verificationStatus")
    availability: Optional[WorkerAvailability] = None
    insurance: Optional[InsuranceSchema] = None

    model_config = {"populate_by_name": True}


# ── Response ────────────────────────────────────────────────────────────────

class WorkerResponse(WorkerBase):
    id: UUID
    user_id: UUID = Field(..., alias="userId")
    cooperative_id: Optional[UUID] = Field(default=None, alias="cooperativeId")
    rating: float = 0.0
    rating_count: int = Field(default=0, alias="ratingCount")
    verification_status: VerificationStatus = Field(..., alias="verificationStatus")
    availability: WorkerAvailability
    location: Optional[LocationSchema] = None
    workload_this_week: int = Field(default=0, alias="workloadThisWeek")
    insurance: InsuranceSchema
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
