from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ReservationStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ReservationBase(BaseModel):
    reservation_time: datetime
    party_size: int = Field(..., gt=0)
    special_requests: Optional[str] = None


class ReservationCreate(ReservationBase):
    restaurant_id: int
    table_id: int


class ReservationUpdate(BaseModel):
    reservation_time: Optional[datetime] = None
    party_size: Optional[int] = Field(None, gt=0)
    status: Optional[ReservationStatus] = None
    special_requests: Optional[str] = None
    table_id: Optional[int] = None


class ReservationResponse(ReservationBase):
    reservation_id: int
    customer_id: int
    restaurant_id: int
    restaurant_name: str
    table_id: int
    status: ReservationStatus
    created_at: datetime
    updated_at: datetime
    confirmation_code: str

    class Config:
        from_attributes = True
