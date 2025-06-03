from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class ReservationSlot(Base):
    __tablename__ = "reservation_slots"

    slot_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(
        Integer, ForeignKey("restaurants.restaurant_id"), nullable=False
    )
    slot_time = Column(DateTime, nullable=False, index=True)
    available_tables = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="reservation_slots")
