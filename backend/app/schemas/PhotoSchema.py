from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RestaurantPhotoBase(BaseModel):
    url: str
    caption: Optional[str] = None
    display_order: int = 0


class RestaurantPhotoCreate(RestaurantPhotoBase):
    pass


class RestaurantPhotoUpdate(BaseModel):
    url: Optional[str] = None
    caption: Optional[str] = None
    display_order: Optional[int] = None


class RestaurantPhotoResponse(RestaurantPhotoBase):
    photo_id: int
    restaurant_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
