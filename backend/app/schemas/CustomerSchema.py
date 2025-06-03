from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.CustomerReviewSchema import ReviewResponse
from app.schemas.ReservationSchema import ReservationResponse
from app.schemas.UserSchema import UserCreate, UserResponse


class NotificationPreference(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    BOTH = "both"


class CustomerBase(BaseModel):
    notification_preference: NotificationPreference = NotificationPreference.EMAIL


class CustomerCreate(CustomerBase):
    user: UserCreate


class CustomerUpdate(BaseModel):
    notification_preference: Optional[NotificationPreference] = None


class CustomerResponse(CustomerBase):
    customer_id: int
    user_id: int
    user: UserResponse

    class Config:
        from_attributes = True


class CustomerDetailResponse(CustomerResponse):
    reservations: List[ReservationResponse] = []
    reviews: List[ReviewResponse] = []

    class Config:
        from_attributes = True
