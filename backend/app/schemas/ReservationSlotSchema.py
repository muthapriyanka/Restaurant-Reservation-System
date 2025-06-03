from datetime import datetime

from pydantic import BaseModel, Field


class ReservationSlotBase(BaseModel):
    slot_time: datetime
    available_tables: int = Field(..., ge=0)
    is_active: bool = True


class ReservationSlotCreate(ReservationSlotBase):
    pass  # restaurant_id comes from path, not here


class ReservationSlotResponse(ReservationSlotBase):
    slot_id: int
    restaurant_id: int

    class Config:
        from_attributes = True
