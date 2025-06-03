from datetime import datetime, time
from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel, EmailStr, Field, validator

from app.schemas.CustomerReviewSchema import ReviewResponse
from app.schemas.OperatingHoursSchema import OperatingHoursResponse
from app.schemas.PhotoSchema import RestaurantPhotoResponse
from app.schemas.TableSchema import TableResponse


class CuisineType(str, Enum):
    ITALIAN = "italian"
    CHINESE = "chinese"
    INDIAN = "indian"
    JAPANESE = "japanese"
    MEXICAN = "mexican"
    FRENCH = "french"
    AMERICAN = "american"
    THAI = "thai"
    MEDITERRANEAN = "mediterranean"
    OTHER = "other"


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    phone_number: str
    email: EmailStr
    cuisine_type: CuisineType
    cost_rating: int = Field(..., ge=1, le=5)
    availability: Optional[List[str]] = None
    booked_slots: Optional[List[str]] = None

    @validator('availability', 'booked_slots', pre=True)
    def parse_json_string(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return v


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    cuisine_type: Optional[CuisineType] = None
    cost_rating: Optional[int] = Field(None, ge=1, le=5)
    is_approved: Optional[bool] = None
    approved_at: Optional[datetime] = None
    availability: Optional[List[str]] = None
    booked_slots: Optional[List[str]] = None

    @validator('availability', 'booked_slots', pre=True)
    def parse_json_string(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return v

    class Config:
        from_attributes = True


class RestaurantResponse(RestaurantBase):
    restaurant_id: int
    manager_id: int
    avg_rating: float
    is_approved: bool
    approved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    photos: List[RestaurantPhotoResponse] = []
    operating_hours: List[OperatingHoursResponse] = []
    availability: List[str] = Field(default_factory=list)
    booked_slots: List[str] = Field(default_factory=list)

    @validator('availability', 'booked_slots', pre=True)
    def parse_json_string(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v or []

    class Config:
        from_attributes = True


class RestaurantDetailResponse(RestaurantResponse):
    tables: List[TableResponse] = []
    reviews: List[ReviewResponse] = []

    class Config:
        from_attributes = True


class RestaurantSearch(BaseModel):
    date: datetime
    time: time
    party_size: int = Field(..., gt=0)
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    cuisine_type: Optional[CuisineType] = None
    min_rating: Optional[float] = Field(None, ge=1, le=5)
    max_cost_rating: Optional[int] = Field(None, ge=1, le=5)
