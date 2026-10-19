import asyncio
import os
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from types import SimpleNamespace

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import (
    CustomerModel,
    CustomerReviewModel,
    OperatingHoursModel,
    PhotoModel,
    ReservationModel,
    ReservationSlotModel,
    RestaurantManagerModel,
    RestaurantModel,
    TableModel,
    UserModel,
)
from app.routes import reservation as reservation_routes
from app.schemas.ReservationSchema import ReservationCreate


class ReservationConcurrencyTest(unittest.TestCase):
    def setUp(self):
        database_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        database_file.close()
        self.database_path = database_file.name
        self.engine = create_engine(
            f"sqlite:///{self.database_path}",
            connect_args={"check_same_thread": False, "timeout": 30},
        )
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)
        self._seed_data()
        self.original_email_sender = reservation_routes.send_email_notification
        reservation_routes.send_email_notification = lambda *_args, **_kwargs: True

    def tearDown(self):
        reservation_routes.send_email_notification = self.original_email_sender
        self.engine.dispose()
        os.unlink(self.database_path)

    def _seed_data(self):
        db = self.Session()
        try:
            manager_user = UserModel.User(
                email="manager@example.com",
                password_hash="unused",
                first_name="Test",
                last_name="Manager",
                role=UserModel.UserRole.RESTAURANT_MANAGER,
            )
            customer_users = [
                UserModel.User(
                    email=f"customer{number}@example.com",
                    password_hash="unused",
                    first_name="Test",
                    last_name=f"Customer {number}",
                    role=UserModel.UserRole.CUSTOMER,
                )
                for number in (1, 2)
            ]
            db.add_all([manager_user, *customer_users])
            db.flush()

            manager = RestaurantManagerModel.RestaurantManager(
                user_id=manager_user.user_id
            )
            customers = [
                CustomerModel.Customer(user_id=user.user_id) for user in customer_users
            ]
            db.add_all([manager, *customers])
            db.flush()

            restaurant = RestaurantModel.Restaurant(
                manager_id=manager.manager_id,
                name="Concurrency Test Restaurant",
                address_line1="1 Test Street",
                city="San Jose",
                state="CA",
                zip_code="95113",
                phone_number="4085550100",
                email="restaurant@example.com",
                cuisine_type=RestaurantModel.CuisineType.AMERICAN,
                cost_rating=2,
                is_approved=True,
            )
            db.add(restaurant)
            db.flush()

            table = TableModel.Table(
                restaurant_id=restaurant.restaurant_id,
                table_number="T1",
                capacity=4,
                is_active=True,
            )
            db.add(table)
            db.commit()

            self.restaurant_id = restaurant.restaurant_id
            self.table_id = table.table_id
            self.customer_users = [
                {"user_id": user.user_id, "email": user.email, "role": "customer"}
                for user in customer_users
            ]
        finally:
            db.close()

    def _book(self, user, reservation_time, barrier=None):
        db = self.Session()
        request = SimpleNamespace(state=SimpleNamespace(user=user))
        payload = ReservationCreate(
            restaurant_id=self.restaurant_id,
            table_id=self.table_id,
            reservation_time=reservation_time,
            party_size=2,
        )
        try:
            if barrier:
                barrier.wait(timeout=5)
            asyncio.run(reservation_routes.book_table(payload, request, db))
            return 201
        except HTTPException as error:
            return error.status_code
        finally:
            db.close()

    def test_simultaneous_requests_create_one_confirmed_reservation(self):
        reservation_time = datetime.now() + timedelta(days=1)
        barrier = threading.Barrier(2)

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(
                executor.map(
                    lambda user: self._book(user, reservation_time, barrier),
                    self.customer_users,
                )
            )

        self.assertEqual(sorted(results), [201, 409])

        db = self.Session()
        try:
            confirmed_count = (
                db.query(ReservationModel.Reservation)
                .filter(
                    ReservationModel.Reservation.table_id == self.table_id,
                    ReservationModel.Reservation.reservation_time == reservation_time,
                    ReservationModel.Reservation.status
                    == ReservationModel.ReservationStatus.CONFIRMED,
                )
                .count()
            )
            self.assertEqual(confirmed_count, 1)
        finally:
            db.close()

    def test_same_table_can_be_reserved_at_different_times(self):
        first_time = datetime.now() + timedelta(days=1)
        second_time = first_time + timedelta(hours=1)

        first_result = self._book(self.customer_users[0], first_time)
        second_result = self._book(self.customer_users[1], second_time)

        self.assertEqual([first_result, second_result], [201, 201])

    def test_cancelled_reservation_releases_table_time(self):
        reservation_time = datetime.now() + timedelta(days=1)
        db = self.Session()
        try:
            customer = (
                db.query(CustomerModel.Customer)
                .filter(
                    CustomerModel.Customer.user_id == self.customer_users[0]["user_id"]
                )
                .one()
            )
            db.add(
                ReservationModel.Reservation(
                    customer_id=customer.customer_id,
                    restaurant_id=self.restaurant_id,
                    table_id=self.table_id,
                    reservation_time=reservation_time,
                    party_size=2,
                    status=ReservationModel.ReservationStatus.CANCELLED,
                    confirmation_code="CANCELLED1",
                )
            )
            db.commit()
        finally:
            db.close()

        result = self._book(self.customer_users[1], reservation_time)

        self.assertEqual(result, 201)


if __name__ == "__main__":
    unittest.main()
