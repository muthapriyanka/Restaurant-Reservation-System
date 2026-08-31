import os
import time as time_module
from datetime import datetime, time

from passlib.context import CryptContext
from sqlalchemy.exc import OperationalError

from app.database import Base, SessionLocal, engine
from app.schemas.OperatingHoursSchema import DayOfWeek

# import all the models
from app.models import (
    AdminModel,
    CustomerModel,
    CustomerReviewModel,
    OperatingHoursModel,
    ReservationModel,
    ReservationSlotModel,
    RestaurantManagerModel,
    RestaurantModel,
    TableModel,
    UserModel,
    PhotoModel,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def wait_for_database(max_attempts=30, delay_seconds=5):
    for attempt in range(1, max_attempts + 1):
        try:
            with engine.connect():
                print("Database connection ready.")
                return
        except OperationalError as exc:
            if attempt == max_attempts:
                print("Database connection failed after retries.")
                raise

            print(
                "Database not ready "
                f"(attempt {attempt}/{max_attempts}): {exc.orig}"
            )
            time_module.sleep(delay_seconds)


DEMO_RESTAURANTS = [
    {
        "name": "Golden Gate Bistro",
        "description": "California comfort food with seasonal small plates.",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94102",
        "address_line1": "120 Market Street",
        "phone_number": "4155551200",
        "email": "hello@goldengatebistro.demo",
        "cuisine_type": RestaurantModel.CuisineType.AMERICAN,
        "cost_rating": 3,
        "avg_rating": 4.6,
    },
    {
        "name": "Saffron Table",
        "description": "Modern Indian dining with vegetarian-friendly plates.",
        "city": "San Jose",
        "state": "CA",
        "zip_code": "95113",
        "address_line1": "88 Santa Clara Street",
        "phone_number": "4085558800",
        "email": "reservations@saffrontable.demo",
        "cuisine_type": RestaurantModel.CuisineType.INDIAN,
        "cost_rating": 2,
        "avg_rating": 4.8,
    },
    {
        "name": "Harbor Sushi",
        "description": "Fresh sushi, sashimi, and chef-selected omakase sets.",
        "city": "Seattle",
        "state": "WA",
        "zip_code": "98101",
        "address_line1": "42 Pike Place",
        "phone_number": "2065554200",
        "email": "book@harborsushi.demo",
        "cuisine_type": RestaurantModel.CuisineType.JAPANESE,
        "cost_rating": 4,
        "avg_rating": 4.7,
    },
]

DEMO_AVAILABILITY = [
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
]


def get_or_create_user(db, email, role):
    user = db.query(UserModel.User).filter(UserModel.User.email == email).first()
    if user:
        return user

    user = UserModel.User(
        email=email,
        password_hash=pwd_context.hash("Password123"),
        phone_number="1234567890",
        first_name="Demo",
        last_name=role.name.title().replace("_", " "),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def seed_demo_data():
    db = SessionLocal()
    try:
        manager_user = get_or_create_user(
            db,
            "demo.manager@example.com",
            UserModel.UserRole.RESTAURANT_MANAGER,
        )
        manager = (
            db.query(RestaurantManagerModel.RestaurantManager)
            .filter(
                RestaurantManagerModel.RestaurantManager.user_id
                == manager_user.user_id
            )
            .first()
        )
        if not manager:
            manager = RestaurantManagerModel.RestaurantManager(
                user_id=manager_user.user_id,
                approved_at=datetime.utcnow(),
            )
            db.add(manager)
            db.commit()
            db.refresh(manager)

        customer_user = get_or_create_user(
            db,
            "demo.customer@example.com",
            UserModel.UserRole.CUSTOMER,
        )
        customer = (
            db.query(CustomerModel.Customer)
            .filter(CustomerModel.Customer.user_id == customer_user.user_id)
            .first()
        )
        if not customer:
            customer = CustomerModel.Customer(
                user_id=customer_user.user_id,
                notification_preference=CustomerModel.NotificationPreference.EMAIL,
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)

        for restaurant_data in DEMO_RESTAURANTS:
            restaurant = (
                db.query(RestaurantModel.Restaurant)
                .filter(RestaurantModel.Restaurant.name == restaurant_data["name"])
                .first()
            )
            if not restaurant:
                restaurant = RestaurantModel.Restaurant(
                    manager_id=manager.manager_id,
                    address_line2=None,
                    is_approved=True,
                    approved_at=datetime.utcnow(),
                    availability=DEMO_AVAILABILITY,
                    booked_slots=[],
                    **restaurant_data,
                )
                db.add(restaurant)
                db.commit()
                db.refresh(restaurant)

            if not restaurant.tables:
                for table_number, capacity in [("T1", 2), ("T2", 4), ("T3", 6)]:
                    db.add(
                        TableModel.Table(
                            restaurant_id=restaurant.restaurant_id,
                            table_number=table_number,
                            capacity=capacity,
                            is_active=True,
                        )
                    )

            if not restaurant.operating_hours:
                for day in [
                    DayOfWeek.MONDAY,
                    DayOfWeek.TUESDAY,
                    DayOfWeek.WEDNESDAY,
                    DayOfWeek.THURSDAY,
                    DayOfWeek.FRIDAY,
                    DayOfWeek.SATURDAY,
                    DayOfWeek.SUNDAY,
                ]:
                    db.add(
                        OperatingHoursModel.OperatingHours(
                            restaurant_id=restaurant.restaurant_id,
                            day_of_week=day,
                            opening_time=time(10, 0),
                            closing_time=time(22, 0),
                        )
                    )

            if not restaurant.reviews:
                db.add(
                    CustomerReviewModel.Review(
                        customer_id=customer.customer_id,
                        restaurant_id=restaurant.restaurant_id,
                        rating=5,
                        comment="Great food and smooth reservation experience.",
                    )
                )

            db.commit()

        print("Demo data seeded successfully!")
    finally:
        db.close()


print("Dropping old tables...")
# Base.metadata.drop_all(engine)  # Deletes existing tables
print("Recreating tables...")
wait_for_database(
    max_attempts=int(os.getenv("DB_STARTUP_MAX_ATTEMPTS", "30")),
    delay_seconds=int(os.getenv("DB_STARTUP_DELAY_SECONDS", "5")),
)
Base.metadata.create_all(engine)  # Creates new tables
print("Tables successfully created!")
seed_demo_data()
