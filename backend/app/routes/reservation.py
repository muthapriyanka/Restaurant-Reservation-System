import random
import string
from datetime import datetime
from typing import Any, Dict, List
from app.routes.email import send_email_notification  # Import your email function


from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app import database
from app.models import (
    CustomerModel,
    ReservationModel,
    RestaurantManagerModel,
    RestaurantModel,
    TableModel,
)
from app.models.ReservationSlotModel import ReservationSlot
from app.models.RestaurantModel import Restaurant
from app.schemas import ReservationSchema
from app.schemas.ReservationSlotSchema import ReservationSlotResponse

router = APIRouter()


@router.post(
    "/reservations",
    response_model=ReservationSchema.ReservationResponse,
    status_code=201,
)
async def book_table(
    reservation: ReservationSchema.ReservationCreate,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # Verify that the current user is a customer
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(
            status_code=403, detail="Not authorized to book reservations"
        )

    # 1) Find the Customer record
    customer = (
        db.query(CustomerModel.Customer)
        .filter(CustomerModel.Customer.user_id == user["user_id"])
        .first()
    )
    if not customer:
        raise HTTPException(404, "Customer record not found")

    # 2) Verify the Table is valid and active
    table = (
        db.query(TableModel.Table)
        .filter(
            TableModel.Table.table_id == reservation.table_id,
            TableModel.Table.restaurant_id == reservation.restaurant_id,
        )
        .first()
    )
    if not table or not table.is_active:
        raise HTTPException(404, "Table not available for reservations")

    # If the table is found, deactivate it to prevent double booking
    table.is_active = False
    db.add(table)


    # 5) Generate a confirmation code
    confirmation_code = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )

    # Create the reservation record
    new_reservation = ReservationModel.Reservation(
        customer_id=customer.customer_id,
        restaurant_id=reservation.restaurant_id,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        party_size=reservation.party_size,
        special_requests=reservation.special_requests,
        confirmation_code=confirmation_code,
    )
    db.add(new_reservation)

    db.commit()
    db.refresh(new_reservation)

    # Get restaurant name for the response
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.restaurant_id == reservation.restaurant_id)
        .first()
    )
    
    # Create response with restaurant name
    response_dict = {
        **new_reservation.__dict__,
        "restaurant_name": restaurant.name if restaurant else None
    }

       # --- EMAIL NOTIFICATION LOGIC STARTS HERE ---
    # Get user info (email, name)
    user_obj = (
        db.query(CustomerModel.Customer)
        .filter(CustomerModel.Customer.customer_id == new_reservation.customer_id)
        .first()
    )
    user_email = user["email"]  # or user_obj.email if available
    user_name = user.get("first_name", "Customer")

    subject = f"Booking Confirmation - {restaurant.name}"
    body = f"""
    <html>
        <body>
            <h2>Booking Confirmation</h2>
            <p>Dear {user_name},</p>
            <p>Your table has been successfully booked at {restaurant.name}.</p>
            <h3>Booking Details:</h3>
            <ul>
                <li>Restaurant: {restaurant.name}</li>
                <li>Date: {new_reservation.reservation_time.strftime('%Y-%m-%d')}</li>
                <li>Time: {new_reservation.reservation_time.strftime('%H:%M')}</li>
                <li>Party Size: {new_reservation.party_size}</li>
                <li>Confirmation Code: {new_reservation.confirmation_code}</li>
            </ul>
            <p>Special Requests: {new_reservation.special_requests or 'None'}</p>
            <p>Restaurant Address: {restaurant.address_line1}, {restaurant.city}, {restaurant.state} {restaurant.zip_code}</p>
            <p>Restaurant Phone: {restaurant.phone_number}</p>
            <p>Thank you for choosing BookTable!</p>
        </body>
    </html>
    """

    # Send the email (handle exceptions gracefully)
    try:
        send_email_notification(user_email, subject, body)
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")

    # --- END EMAIL LOGIC ---
    return response_dict


@router.get(
    "/restaurants/{restaurant_id}/availability",
    response_model=List[ReservationSlotResponse],
)
async def get_availability(
    restaurant_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # 1) Only customers may view availability
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(403, "Not authorized to view availability")

    # 2) Ensure the restaurant exists
    restaurant = (
        db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    )
    if not restaurant:
        raise HTTPException(404, "Restaurant not found")

    # 3) Fetch active slots with at least one table left, ordered by time
    now = datetime.utcnow()
    slots = (
        db.query(ReservationSlot)
        .filter(
            ReservationSlot.restaurant_id == restaurant_id,
            ReservationSlot.is_active == True,
            ReservationSlot.available_tables > 0,
            ReservationSlot.slot_time >= now,  # only future (or current) slots
        )
        .order_by(ReservationSlot.slot_time)
        .all()
    )

    return slots


@router.get(
    "/reservations",
    response_model=List[ReservationSchema.ReservationResponse],
)
async def list_reservations(
    request: Request,
    db: Session = Depends(database.get_db),
):
    # Only customers may view their own reservations
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(403, "Not authorized to view reservations")

    # Fetch the Customer record
    customer = (
        db.query(CustomerModel.Customer)
        .filter(CustomerModel.Customer.user_id == user["user_id"])
        .first()
    )
    if not customer:
        raise HTTPException(404, "Customer record not found")

    # Retrieve all reservations for this customer with restaurant information
    reservations = (
        db.query(ReservationModel.Reservation, RestaurantModel.Restaurant.name)
        .join(
            RestaurantModel.Restaurant,
            ReservationModel.Reservation.restaurant_id == RestaurantModel.Restaurant.restaurant_id
        )
        .filter(ReservationModel.Reservation.customer_id == customer.customer_id)
        .order_by(ReservationModel.Reservation.reservation_time)
        .all()
    )

    # Transform the results to include restaurant name
    result = []
    for reservation, restaurant_name in reservations:
        reservation_dict = {
            **reservation.__dict__,
            "restaurant_name": restaurant_name
        }
        result.append(reservation_dict)

    return result


@router.get(
    "/reservations/{reservation_id}",
    response_model=ReservationSchema.ReservationResponse,
)
async def get_reservation_detail(
    reservation_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # Only customers may view their own reservation details
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(403, "Not authorized to view reservation details")

    # Fetch the Customer record
    customer = (
        db.query(CustomerModel.Customer)
        .filter(CustomerModel.Customer.user_id == user["user_id"])
        .first()
    )
    if not customer:
        raise HTTPException(404, "Customer record not found")

    # Retrieve the specific reservation and ensure it belongs to this customer
    reservation = (
        db.query(ReservationModel.Reservation)
        .filter(
            ReservationModel.Reservation.reservation_id == reservation_id,
            ReservationModel.Reservation.customer_id == customer.customer_id,
        )
        .first()
    )
    if not reservation:
        raise HTTPException(404, "Reservation not found")

    return reservation


@router.put(
    "/reservations/{reservation_id}",
    response_model=ReservationSchema.ReservationResponse,
)
async def update_reservation(
    reservation_id: int,
    update_data: ReservationSchema.ReservationUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # 1) Only customers may update their own reservations
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(403, "Not authorized to update reservations")

    # 2) Fetch the Customer record
    customer = (
        db.query(CustomerModel.Customer)
        .filter(CustomerModel.Customer.user_id == user["user_id"])
        .first()
    )
    if not customer:
        raise HTTPException(404, "Customer record not found")

    # 3) Retrieve the reservation and ensure ownership
    reservation = (
        db.query(ReservationModel.Reservation)
        .filter(
            ReservationModel.Reservation.reservation_id == reservation_id,
            ReservationModel.Reservation.customer_id == customer.customer_id,
        )
        .first()
    )
    if not reservation:
        raise HTTPException(404, "Reservation not found")

    # 4) Prevent customers from changing status
    if update_data.status is not None:
        raise HTTPException(403, "Cannot modify reservation status")

    # 5) If table_id or reservation_time is changing, re-validate availability
    new_table_id = update_data.table_id or reservation.table_id
    new_time = update_data.reservation_time or reservation.reservation_time

    # 5a) Validate new table
    table = (
        db.query(TableModel.Table)
        .filter(
            TableModel.Table.table_id == new_table_id,
            TableModel.Table.restaurant_id == reservation.restaurant_id,
        )
        .first()
    )
    if not table or not table.is_active:
        raise HTTPException(404, "Table not available for reservations")

    # 5b) Validate the corresponding slot
    slot = (
        db.query(ReservationSlot)
        .filter(
            ReservationSlot.restaurant_id == reservation.restaurant_id,
            ReservationSlot.slot_time == new_time,
            ReservationSlot.is_active == True,
        )
        .with_for_update()
        .first()
    )
    if not slot or slot.available_tables < 1:
        raise HTTPException(400, "No available tables at this time slot")

    # 5c) Decrement the slot's counter (and deactivate if zero)
    slot.available_tables -= 1
    if slot.available_tables == 0:
        slot.is_active = False
    db.add(slot)

    # 6) Apply updates for allowed fields
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(reservation, field, value)

    db.commit()
    db.refresh(reservation)
    return reservation


@router.delete(
    "/reservations/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_reservation(
    reservation_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # 1) Only customers may cancel their own reservations
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(
            status_code=403, detail="Not authorized to cancel reservations"
        )

    # 2) Fetch the Customer record
    customer = (
        db.query(CustomerModel.Customer)
        .filter(CustomerModel.Customer.user_id == user["user_id"])
        .first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer record not found")

    # 3) Retrieve the reservation and ensure ownership
    reservation = (
        db.query(ReservationModel.Reservation)
        .filter(
            ReservationModel.Reservation.reservation_id == reservation_id,
            ReservationModel.Reservation.customer_id == customer.customer_id,
        )
        .first()
    )
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # 4) If already cancelled or completed, do nothing (idempotent)
    if reservation.status == ReservationModel.ReservationStatus.CANCELLED:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # 5) Update status to CANCELLED
    reservation.status = ReservationModel.ReservationStatus.CANCELLED

    # 6) Reactivate the table
    table = (
        db.query(TableModel.Table)
        .filter(
            TableModel.Table.table_id == reservation.table_id,
            TableModel.Table.restaurant_id == reservation.restaurant_id,
        )
        .first()
    )
    if table:
        table.is_active = True
        db.add(table)


    # 8) Commit all changes
    db.commit()

    # 9) Return no content
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _verify_manager_restaurant(db: Session, manager_user_id: int, restaurant_id: int):
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .join(RestaurantManagerModel.RestaurantManager)
        .filter(
            RestaurantModel.Restaurant.restaurant_id == restaurant_id,
            RestaurantManagerModel.RestaurantManager.user_id == manager_user_id,
        )
        .first()
    )
    if not restaurant:
        raise HTTPException(404, "Restaurant not found or not managed by you")
    return restaurant


# Manager routes for reservations
@router.get(
    "/manager/restaurants/{restaurant_id}/reservations",
    response_model=List[ReservationSchema.ReservationResponse],
)
async def list_all_reservations(
    restaurant_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # Only restaurant managers may list reservations
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(403, "Not authorized to view reservations")

    # Verify manager owns this restaurant
    _verify_manager_restaurant(db, user["user_id"], restaurant_id)

    # Fetch all reservations for the restaurant
    reservations = (
        db.query(ReservationModel.Reservation)
        .filter(ReservationModel.Reservation.restaurant_id == restaurant_id)
        .order_by(ReservationModel.Reservation.reservation_time)
        .all()
    )
    return reservations


@router.get(
    "/manager/restaurants/{restaurant_id}/reservations/{reservation_id}",
    response_model=ReservationSchema.ReservationResponse,
)
async def get_reservation_detail(
    restaurant_id: int,
    reservation_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # Only restaurant managers may view reservation details
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(403, "Not authorized to view reservation details")

    # Verify manager owns this restaurant
    _verify_manager_restaurant(db, user["user_id"], restaurant_id)

    # Fetch the specific reservation
    reservation = (
        db.query(ReservationModel.Reservation)
        .filter(
            ReservationModel.Reservation.restaurant_id == restaurant_id,
            ReservationModel.Reservation.reservation_id == reservation_id,
        )
        .first()
    )
    if not reservation:
        raise HTTPException(404, "Reservation not found")

    return reservation


@router.put(
    "/manager/restaurants/{restaurant_id}/reservations/{reservation_id}",
    response_model=ReservationSchema.ReservationResponse,
)
async def update_reservation_status(
    restaurant_id: int,
    reservation_id: int,
    update_data: ReservationSchema.ReservationUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # 1) Only restaurant managers may update status
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(403, "Not authorized to update reservation status")

    # 2) Verify manager owns this restaurant
    _verify_manager_restaurant(db, user["user_id"], restaurant_id)

    # 3) Fetch the reservation within this restaurant
    reservation = (
        db.query(ReservationModel.Reservation)
        .filter(
            ReservationModel.Reservation.restaurant_id == restaurant_id,
            ReservationModel.Reservation.reservation_id == reservation_id,
        )
        .first()
    )
    if not reservation:
        raise HTTPException(404, "Reservation not found")

    # 4) Only allow status field in payload
    data: Dict[str, Any] = update_data.dict(exclude_unset=True)
    if not data or set(data.keys()) != {"status"}:
        raise HTTPException(400, "Must supply exactly one field: status")

    # 5) Apply the status update
    reservation.status = data["status"]

    db.commit()
    db.refresh(reservation)
    return reservation
