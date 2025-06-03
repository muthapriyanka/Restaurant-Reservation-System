import enum
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import (
    CustomerReviewModel,
    OperatingHoursModel,
    ReservationSlotModel,
    RestaurantManagerModel,
    TableModel,
)


class CuisineType(enum.Enum):
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


class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(
        Integer, ForeignKey("restaurant_managers.manager_id"), nullable=False
    )
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    address_line1 = Column(String(100), nullable=False)
    address_line2 = Column(String(100))
    city = Column(String(50), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    zip_code = Column(String(20), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    cuisine_type = Column(Enum(CuisineType), nullable=False, index=True)
    cost_rating = Column(Integer, nullable=False)  # 1-5
    avg_rating = Column(Float, default=0.0)
    is_approved = Column(Boolean, default=False)
    approved_at = Column(DateTime, nullable=True)
    availability = Column(JSON, nullable=True, default=list)  # Store available time slots
    booked_slots = Column(JSON, nullable=True, default=list)  # Store booked time slots
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    manager = relationship("RestaurantManager", back_populates="restaurants")
    photos = relationship("RestaurantPhoto", back_populates="restaurant")
    operating_hours = relationship("OperatingHours", back_populates="restaurant")
    tables = relationship("Table", back_populates="restaurant")
    reservation_slots = relationship("ReservationSlot", back_populates="restaurant")
    reservations = relationship("Reservation", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")