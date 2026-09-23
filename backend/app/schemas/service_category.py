"""
Pydantic schemas for ServiceCategory.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


# ── Base ────────────────────────────────────────────────────────────────────

class ServiceCategoryBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    icon: Optional[str] = None
    base_visit_charge: float = Field(default=0.0, alias="baseVisitCharge", ge=0)

    model_config = {"populate_by_name": True}


# ── Create ──────────────────────────────────────────────────────────────────

class ServiceCategoryCreate(ServiceCategoryBase):
    pass


# ── Update ──────────────────────────────────────────────────────────────────

class ServiceCategoryUpdate(BaseModel):
    key: Optional[str] = Field(default=None, min_length=1, max_length=50)
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    icon: Optional[str] = None
    base_visit_charge: Optional[float] = Field(default=None, alias="baseVisitCharge", ge=0)

    model_config = {"populate_by_name": True}


# ── Response ────────────────────────────────────────────────────────────────

class ServiceCategoryResponse(ServiceCategoryBase):
    id: UUID
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
