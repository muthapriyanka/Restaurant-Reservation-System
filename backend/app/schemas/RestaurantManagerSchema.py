from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.UserSchema import UserCreate, UserResponse


class RestaurantManagerBase(BaseModel):
    pass


class RestaurantManagerCreate(RestaurantManagerBase):
    user: UserCreate


class RestaurantManagerUpdate(BaseModel):
    approved_at: Optional[datetime] = None


class RestaurantManagerResponse(RestaurantManagerBase):
    manager_id: int
    user_id: int
    approved_at: Optional[datetime]
    user: UserResponse

    class Config:
        from_attributes = True
