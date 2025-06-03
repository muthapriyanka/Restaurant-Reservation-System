# from enum import
import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.ReservationModel import Reservation


class NotificationPreference(enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    BOTH = "both"


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)
    notification_preference = Column(
        Enum(NotificationPreference), default=NotificationPreference.EMAIL
    )

    # Relationships
    user = relationship("User", back_populates="customer")
    reservations = relationship("Reservation", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
