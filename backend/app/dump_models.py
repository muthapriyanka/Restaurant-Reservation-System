# # models.py
# from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Time, Enum, ForeignKey, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from datetime import datetime
# import enum

# Base = declarative_base()
"""
# class UserRole(enum.Enum):
#     CUSTOMER = "customer"
#     RESTAURANT_MANAGER = "restaurant_manager"
#     ADMIN = "admin"
"""
"""# class ReservationStatus(enum.Enum):
#     CONFIRMED = "confirmed"
#     CANCELLED = "cancelled"
#     COMPLETED = "completed"
"""
'''# class DayOfWeek(enum.Enum):
#     MONDAY = "monday"
#     TUESDAY = "tuesday"
#     WEDNESDAY = "wednesday"
#     THURSDAY = "thursday"
#     FRIDAY = "friday"
#     SATURDAY = "saturday"
#     SUNDAY = "sunday"'''

'''# class CuisineType(enum.Enum):
#     ITALIAN = "italian"
#     CHINESE = "chinese"
#     INDIAN = "indian"
#     JAPANESE = "japanese"
#     MEXICAN = "mexican"
#     FRENCH = "french"
#     AMERICAN = "american"
#     THAI = "thai"
#     MEDITERRANEAN = "mediterranean"
#     OTHER = "other"'''
"""
# class NotificationPreference(enum.Enum):
#     EMAIL = "email"
#     SMS = "sms"
#     BOTH = "both"
"""
"""
# class User(Base):
#     __tablename__ = "users"

#     user_id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(100), unique=True, index=True, nullable=False)
#     password_hash = Column(String(255), nullable=False)
#     phone_number = Column(String(20))
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String(50), nullable=False)
#     role = Column(Enum(UserRole), nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     customer = relationship("Customer", back_populates="user", uselist=False)
#     restaurant_manager = relationship("RestaurantManager", back_populates="user", uselist=False)
#     admin = relationship("Admin", back_populates="user", uselist=False)
"""
"""
# class Customer(Base):
#     __tablename__ = "customers"

#     customer_id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)
#     notification_preference = Column(Enum(NotificationPreference), default=NotificationPreference.EMAIL)

#     # Relationships
#     user = relationship("User", back_populates="customer")
#     reservations = relationship("Reservation", back_populates="customer")
#     reviews = relationship("Review", back_populates="customer")
"""
"""
# class RestaurantManager(Base):
#     __tablename__ = "restaurant_managers"

#     manager_id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)
#     approved_at = Column(DateTime, nullable=True)

#     # Relationships
#     user = relationship("User", back_populates="restaurant_manager")
#     restaurants = relationship("Restaurant", back_populates="manager")
"""
"""
# class Admin(Base):
#     __tablename__ = "admins"

#     admin_id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)

#     # Relationships
#     user = relationship("User", back_populates="admin")
"""
"""# class Restaurant(Base):
#     __tablename__ = "restaurants"

#     restaurant_id = Column(Integer, primary_key=True, index=True)
#     manager_id = Column(Integer, ForeignKey("restaurant_managers.manager_id"), nullable=False)
#     name = Column(String(100), nullable=False, index=True)
#     description = Column(Text)
#     address_line1 = Column(String(100), nullable=False)
#     address_line2 = Column(String(100))
#     city = Column(String(50), nullable=False, index=True)
#     state = Column(String(50), nullable=False, index=True)
#     zip_code = Column(String(20), nullable=False, index=True)
#     phone_number = Column(String(20), nullable=False)
#     email = Column(String(100), nullable=False)
#     cuisine_type = Column(Enum(CuisineType), nullable=False, index=True)
#     cost_rating = Column(Integer, nullable=False)  # 1-5
#     avg_rating = Column(Float, default=0.0)
#     is_approved = Column(Boolean, default=False)
#     approved_at = Column(DateTime, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     manager = relationship("RestaurantManager", back_populates="restaurants")
#     photos = relationship("RestaurantPhoto", back_populates="restaurant")
#     operating_hours = relationship("OperatingHours", back_populates="restaurant")
#     tables = relationship("Table", back_populates="restaurant")
#     reservation_slots = relationship("ReservationSlot", back_populates="restaurant")
#     reservations = relationship("Reservation", back_populates="restaurant")
#     reviews = relationship("Review", back_populates="restaurant")
"""
"""# class RestaurantPhoto(Base):
#     __tablename__ = "restaurant_photos"

#     photo_id = Column(Integer, primary_key=True, index=True)
#     restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
#     url = Column(String(255), nullable=False)
#     caption = Column(String(255))
#     display_order = Column(Integer, default=0)
#     uploaded_at = Column(DateTime, default=datetime.utcnow)

#     # Relationships
#     restaurant = relationship("Restaurant", back_populates="photos")"""
"""
# class OperatingHours(Base):
#     __tablename__ = "operating_hours"

#     hours_id = Column(Integer, primary_key=True, index=True)
#     restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
#     day_of_week = Column(Enum(DayOfWeek), nullable=False)
#     opening_time = Column(Time, nullable=False)
#     closing_time = Column(Time, nullable=False)

#     # Relationships
#     restaurant = relationship("Restaurant", back_populates="operating_hours")"""

"""# class Table(Base):
#     __tablename__ = "tables"

#     table_id = Column(Integer, primary_key=True, index=True)
#     restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
#     capacity = Column(Integer, nullable=False)
#     table_number = Column(String(20), nullable=False)
#     is_active = Column(Boolean, default=True)

#     # Relationships
#     restaurant = relationship("Restaurant", back_populates="tables")
#     reservations = relationship("Reservation", back_populates="table")
"""
"""# class ReservationSlot(Base):
#     __tablename__ = "reservation_slots"

#     slot_id = Column(Integer, primary_key=True, index=True)
#     restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
#     slot_time = Column(DateTime, nullable=False, index=True)
#     available_tables = Column(Integer, nullable=False, default=0)
#     is_active = Column(Boolean, default=True)

#     # Relationships
#     restaurant = relationship("Restaurant", back_populates="reservation_slots")
"""
"""# class Reservation(Base):
#     __tablename__ = "reservations"

#     reservation_id = Column(Integer, primary_key=True, index=True)
#     customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
#     restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
#     table_id = Column(Integer, ForeignKey("tables.table_id"), nullable=False)
#     reservation_time = Column(DateTime, nullable=False, index=True)
#     party_size = Column(Integer, nullable=False)
#     status = Column(Enum(ReservationStatus), default=ReservationStatus.CONFIRMED)
#     special_requests = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     confirmation_code = Column(String(20), unique=True, index=True, nullable=False)

#     # Relationships
#     customer = relationship("Customer", back_populates="reservations")
#     restaurant = relationship("Restaurant", back_populates="reservations")
#     table = relationship("Table", back_populates="reservations")
"""
"""# class Review(Base):
#     __tablename__ = "reviews"

#     review_id = Column(Integer, primary_key=True, index=True)
#     customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
#     restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
#     rating = Column(Integer, nullable=False)  # 1-5
#     comment = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     customer = relationship("Customer", back_populates="reviews")
#     restaurant = relationship("Restaurant", back_populates="reviews")
"""
