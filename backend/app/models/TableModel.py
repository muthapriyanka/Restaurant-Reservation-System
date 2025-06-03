from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Table(Base):
    __tablename__ = "tables"

    table_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(
        Integer, ForeignKey("restaurants.restaurant_id"), nullable=False
    )
    capacity = Column(Integer, nullable=False)
    table_number = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="tables")
    reservations = relationship("Reservation", back_populates="table")
