import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models import AdminModel, CustomerModel, RestaurantManagerModel


class UserRole(enum.Enum):
    CUSTOMER = "customer"
    RESTAURANT_MANAGER = "restaurant_manager"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone_number = Column(String(20))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="user", uselist=False)
    restaurant_manager = relationship(
        "RestaurantManager", back_populates="user", uselist=False
    )
    admin = relationship("Admin", back_populates="user", uselist=False)
