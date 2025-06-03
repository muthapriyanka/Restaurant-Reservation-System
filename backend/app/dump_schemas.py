# # schemas.py
# from pydantic import BaseModel, EmailStr, Field, validator
# from typing import List, Optional, Dict, Any
# from datetime import datetime, time
# from enum import Enum

# # Enums
"""
# class UserRole(str, Enum):
#     CUSTOMER = "customer"
#     RESTAURANT_MANAGER = "restaurant_manager"
#     ADMIN = "admin"
"""
"""# class ReservationStatus(str, Enum):
#     CONFIRMED = "confirmed"
#     CANCELLED = "cancelled"
#     COMPLETED = "completed"
"""
'''# class DayOfWeek(str, Enum):
#     MONDAY = "monday"
#     TUESDAY = "tuesday"
#     WEDNESDAY = "wednesday"
#     THURSDAY = "thursday"
#     FRIDAY = "friday"
#     SATURDAY = "saturday"
#     SUNDAY = "sunday"'''

"""# class CuisineType(str, Enum):
#     ITALIAN = "italian"
#     CHINESE = "chinese"
#     INDIAN = "indian"
#     JAPANESE = "japanese"
#     MEXICAN = "mexican"
#     FRENCH = "french"
#     AMERICAN = "american"
#     THAI = "thai"
#     MEDITERRANEAN = "mediterranean"
#     OTHER = "other"
"""
# class NotificationPreference(str, Enum):
#     EMAIL = "email"
#     SMS = "sms"
#     BOTH = "both"

# # Base schemas (shared properties)
"""
# class UserBase(BaseModel):
#     email: EmailStr
#     phone_number: Optional[str] = None
#     first_name: str
#     last_name: str
#     role: UserRole
# class CustomerBase(BaseModel):
#     notification_preference: NotificationPreference = NotificationPreference.EMAIL

# class RestaurantManagerBase(BaseModel):
#     pass

# class AdminBase(BaseModel):
#     pass
"""

"""# class RestaurantBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     address_line1: str
#     address_line2: Optional[str] = None
#     city: str
#     state: str
#     zip_code: str
#     phone_number: str
#     email: EmailStr
#     cuisine_type: CuisineType
#     cost_rating: int = Field(..., ge=1, le=5)
"""
"""# class RestaurantPhotoBase(BaseModel):
#     url: str
#     caption: Optional[str] = None
#     display_order: int = 0
"""
"""# class OperatingHoursBase(BaseModel):
#     day_of_week: DayOfWeek
#     opening_time: time
#     closing_time: time

#     @validator('closing_time')
#     def closing_after_opening(cls, v, values):
#         if 'opening_time' in values and v <= values['opening_time']:
#             raise ValueError('closing_time must be after opening_time')
#         return v"""

"""# class TableBase(BaseModel):
#     capacity: int = Field(..., gt=0)
#     table_number: str
#     is_active: bool = True
"""
"""# class ReservationSlotBase(BaseModel):
#     slot_time: datetime
#     available_tables: int = Field(..., ge=0)
#     is_active: bool = True
"""
"""# class ReservationBase(BaseModel):
#     reservation_time: datetime
#     party_size: int = Field(..., gt=0)
#     special_requests: Optional[str] = None
"""
"""# class ReviewBase(BaseModel):
#     rating: int = Field(..., ge=1, le=5)
#     comment: Optional[str] = None
"""
"""# # Create schemas (input for creating new items)
# class UserCreate(UserBase):
#     password: str = Field(..., min_length=8)"""
"""
# class CustomerCreate(CustomerBase):
#     user: UserCreate
""" """
# class RestaurantManagerCreate(RestaurantManagerBase):
#     user: UserCreate
""" """
# class AdminCreate(AdminBase):
#     user: UserCreate
"""
"""# class RestaurantCreate(RestaurantBase):
#     pass
"""
"""# class RestaurantPhotoCreate(RestaurantPhotoBase):
#     restaurant_id: int
"""
"""# class OperatingHoursCreate(OperatingHoursBase):
#     restaurant_id: int
"""
"""# class TableCreate(TableBase):
#     restaurant_id: int
"""
"""# class ReservationSlotCreate(ReservationSlotBase):
#     restaurant_id: int
"""
"""# class ReservationCreate(ReservationBase):
#     restaurant_id: int
"""
"""# class ReviewCreate(ReviewBase):
#     restaurant_id: int
"""
# # Update schemas
"""
# class UserUpdate(BaseModel):
#     email: Optional[EmailStr] = None
#     phone_number: Optional[str] = None
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     role: Optional[UserRole] = None
""" """
# class CustomerUpdate(BaseModel):
#     notification_preference: Optional[NotificationPreference] = None
""" """
# class RestaurantManagerUpdate(BaseModel):
#     approved_at: Optional[datetime] = None
""" """
# class AdminUpdate(BaseModel):
#     pass
"""
"""# class RestaurantUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     address_line1: Optional[str] = None
#     address_line2: Optional[str] = None
#     city: Optional[str] = None
#     state: Optional[str] = None
#     zip_code: Optional[str] = None
#     phone_number: Optional[str] = None
#     email: Optional[EmailStr] = None
#     cuisine_type: Optional[CuisineType] = None
#     cost_rating: Optional[int] = Field(None, ge=1, le=5)
#     is_approved: Optional[bool] = None
#     approved_at: Optional[datetime] = None
"""
"""# class RestaurantPhotoUpdate(BaseModel):
#     url: Optional[str] = None
#     caption: Optional[str] = None
#     display_order: Optional[int] = None
"""
# class OperatingHoursUpdate(BaseModel):
#     opening_time: Optional[time] = None
#     closing_time: Optional[time] = None

#     @validator('closing_time')
#     def closing_after_opening(cls, v, values, **kwargs):
#         if v is not None and 'opening_time' in values and values['opening_time'] is not None and v <= values['opening_time']:
#             raise ValueError('closing_time must be after opening_time')
#         return v

"""# class TableUpdate(BaseModel):
#     capacity: Optional[int] = Field(None, gt=0)
#     table_number: Optional[str] = None
#     is_active: Optional[bool] = None
"""
# class ReservationSlotUpdate(BaseModel):
#     slot_time: Optional[datetime] = None
#     available_tables: Optional[int] = Field(None, ge=0)
#     is_active: Optional[bool] = None

"""# class ReservationUpdate(BaseModel):
#     reservation_time: Optional[datetime] = None
#     party_size: Optional[int] = Field(None, gt=0)
#     status: Optional[ReservationStatus] = None
#     special_requests: Optional[str] = None
#     table_id: Optional[int] = None
"""
# class ReviewUpdate(BaseModel):
#     rating: Optional[int] = Field(None, ge=1, le=5)
#     comment: Optional[str] = None

# # Response schemas
"""
# class UserResponse(UserBase):
#     user_id: int
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True
""" """
# class CustomerResponse(CustomerBase):
#     customer_id: int
#     user_id: int
#     user: UserResponse

#     class Config:
#         from_attributes = True
""" """
# class RestaurantManagerResponse(RestaurantManagerBase):
#     manager_id: int
#     user_id: int
#     approved_at: Optional[datetime]
#     user: UserResponse

#     class Config:
#         from_attributes = True
""" """
# class AdminResponse(AdminBase):
#     admin_id: int
#     user_id: int
#     user: UserResponse

#     class Config:
#         from_attributes = True
"""
"""# class ReviewResponse(ReviewBase):
#     review_id: int
#     customer_id: int
#     restaurant_id: int
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True
"""
"""# class RestaurantPhotoResponse(RestaurantPhotoBase):
#     photo_id: int
#     restaurant_id: int
#     uploaded_at: datetime

#     class Config:
#         from_attributes = True
"""
"""# class OperatingHoursResponse(OperatingHoursBase):
#     hours_id: int
#     restaurant_id: int

#     class Config:
#         from_attributes = True"""

"""# class TableResponse(TableBase):
#     table_id: int
#     restaurant_id: int

#     class Config:
#         from_attributes = True
"""
# class ReservationSlotResponse(ReservationSlotBase):
#     slot_id: int
#     restaurant_id: int

#     class Config:
#         from_attributes = True

"""# class ReservationResponse(ReservationBase):
#     reservation_id: int
#     customer_id: int
#     restaurant_id: int
#     table_id: int
#     status: ReservationStatus
#     created_at: datetime
#     updated_at: datetime
#     confirmation_code: str

#     class Config:
#         from_attributes = True
"""
"""# class RestaurantResponse(RestaurantBase):
#     restaurant_id: int
#     manager_id: int
#     avg_rating: float
#     is_approved: bool
#     approved_at: Optional[datetime]
#     created_at: datetime
#     updated_at: datetime
#     photos: List[RestaurantPhotoResponse] = []
#     operating_hours: List[OperatingHoursResponse] = []

#     class Config:
#         from_attributes = True
"""
# # Extended response schemas with relationships
"""# class RestaurantDetailResponse(RestaurantResponse):
#     tables: List[TableResponse] = []
#     reviews: List[ReviewResponse] = []

#     class Config:
#         from_attributes = True"""
"""
# class CustomerDetailResponse(CustomerResponse):
#     reservations: List[ReservationResponse] = []
#     reviews: List[ReviewResponse] = []

#     class Config:
#         from_attributes = True
"""
# # Search and filter schemas
"""# class RestaurantSearch(BaseModel):
#     date: datetime
#     time: time
#     party_size: int = Field(..., gt=0)
#     city: Optional[str] = None
#     state: Optional[str] = None
#     zip_code: Optional[str] = None
#     cuisine_type: Optional[CuisineType] = None
#     min_rating: Optional[float] = Field(None, ge=1, le=5)
#     max_cost_rating: Optional[int] = Field(None, ge=1, le=5)
"""
# # Auth schemas
# class Token(BaseModel):
#     access_token: str
#     token_type: str = "bearer"

# class TokenData(BaseModel):
#     user_id: Optional[int] = None
#     role: Optional[UserRole] = None

# # Analytics schemas
# class ReservationAnalytics(BaseModel):
#     total_reservations: int
#     reservations_by_day: Dict[str, int]
#     average_party_size: float
#     most_popular_cuisine: Optional[str]
#     most_popular_restaurants: List[Dict[str, Any]]
#     reservation_status_counts: Dict[str, int]
