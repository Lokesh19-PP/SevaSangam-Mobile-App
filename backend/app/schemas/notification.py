"""
Pydantic schemas for Notification.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


# ── Base ────────────────────────────────────────────────────────────────────

class NotificationBase(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    title_key: str = Field(..., alias="titleKey", min_length=1, max_length=100)
    body: Optional[str] = None

    model_config = {"populate_by_name": True}


# ── Create ──────────────────────────────────────────────────────────────────

class NotificationCreate(NotificationBase):
    user_id: UUID = Field(..., alias="userId")


# ── Update ──────────────────────────────────────────────────────────────────

class NotificationUpdate(BaseModel):
    read: Optional[bool] = None


# ── Response ────────────────────────────────────────────────────────────────

class NotificationResponse(NotificationBase):
    id: UUID
    user_id: UUID = Field(..., alias="userId")
    read: bool = False
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
