import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class ReservationStatus(enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    restaurant_id = Column(
        Integer, ForeignKey("restaurants.restaurant_id"), nullable=False
    )
    table_id = Column(Integer, ForeignKey("tables.table_id"), nullable=False)
    reservation_time = Column(DateTime, nullable=False, index=True)
    party_size = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.CONFIRMED)
    special_requests = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmation_code = Column(String(20), unique=True, index=True, nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")
    table = relationship("Table", back_populates="reservations")
