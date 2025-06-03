from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class RestaurantPhoto(Base):
    __tablename__ = "restaurant_photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(
        Integer, ForeignKey("restaurants.restaurant_id"), nullable=False
    )
    url = Column(String(255), nullable=False)
    caption = Column(String(255))
    display_order = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="photos")
