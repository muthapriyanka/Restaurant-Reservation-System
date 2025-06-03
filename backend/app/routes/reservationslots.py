from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.OperatingHoursModel import OperatingHours
from app.models.ReservationSlotModel import ReservationSlot
from app.models.RestaurantModel import Restaurant
from app.schemas.ReservationSlotSchema import (
    ReservationSlotCreate,
    ReservationSlotResponse,
)

router = APIRouter(prefix="/manager")


@router.post(
    "/restaurants/{restaurant_id}/slots", response_model=ReservationSlotResponse
)
async def create_reservation_slot(
    restaurant_id: int,
    reservation_data: ReservationSlotCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    # Check user role
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to create reservation slots"
        )

    # Check if restaurant exists
    restaurant = (
        db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Get the day of the week for the slot_time
    from datetime import datetime

    day_of_week = reservation_data.slot_time.strftime("%A").upper()

    # Check if the slot_time falls within the operating hours
    operating_hours = (
        db.query(OperatingHours)
        .filter(
            OperatingHours.restaurant_id == restaurant_id,
            OperatingHours.day_of_week == day_of_week,
        )
        .first()
    )

    if not operating_hours:
        raise HTTPException(
            status_code=400, detail=f"No operating hours found for {day_of_week}"
        )

    if not (
        operating_hours.opening_time
        <= reservation_data.slot_time.time()
        <= operating_hours.closing_time
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Slot time {reservation_data.slot_time} is outside the operating hours ({operating_hours.opening_time} - {operating_hours.closing_time})",
        )

    # Optional: Add logic to prevent duplicate slots at the same time
    existing_slot = (
        db.query(ReservationSlot)
        .filter(
            ReservationSlot.restaurant_id == restaurant_id,
            ReservationSlot.slot_time == reservation_data.slot_time,
        )
        .first()
    )
    if existing_slot:
        raise HTTPException(
            status_code=400,
            detail="A slot at this time already exists for the restaurant",
        )

    # Create slot
    new_slot = ReservationSlot(
        restaurant_id=restaurant_id,
        slot_time=reservation_data.slot_time,
        available_tables=reservation_data.available_tables,
        is_active=reservation_data.is_active,
    )

    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)

    return new_slot


@router.get(
    "/restaurants/{restaurant_id}/slots",
    response_model=List[ReservationSlotResponse],
    summary="Get all reservation slots for a restaurant",
)
async def get_reservation_slots(
    restaurant_id: int, db: Session = Depends(get_db), request: Request = None
):
    # Verify the user's role
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view reservation slots",
        )

    # Check if the restaurant exists
    restaurant = (
        db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
        )

    # Retrieve all slots for the restaurant
    slots = (
        db.query(ReservationSlot)
        .filter(ReservationSlot.restaurant_id == restaurant_id)
        .all()
    )
    return slots


# PUT /api/manager/restaurants/{restaurant_id}/slots/{slot_id} - Update a reservation slot
@router.put(
    "/restaurants/{restaurant_id}/slots/{slot_id}",
    response_model=ReservationSlotResponse,
    summary="Update an existing reservation slot",
)
async def update_reservation_slot(
    restaurant_id: int,
    slot_id: int,
    reservation_data: ReservationSlotCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    # Verify the user's role
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update reservation slots",
        )

    # Validate that the restaurant exists
    restaurant = (
        db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
        )

    # Retrieve the slot to be updated
    slot = (
        db.query(ReservationSlot)
        .filter(
            ReservationSlot.restaurant_id == restaurant_id,
            ReservationSlot.slot_id == slot_id,
        )
        .first()
    )
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation slot not found"
        )

    # Validate the slot_time against operating hours
    day_of_week = reservation_data.slot_time.strftime("%A").upper()
    operating_hours = (
        db.query(OperatingHours)
        .filter(
            OperatingHours.restaurant_id == restaurant_id,
            OperatingHours.day_of_week == day_of_week,
        )
        .first()
    )
    if not operating_hours:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No operating hours found for {day_of_week}",
        )
    if not (
        operating_hours.opening_time
        <= reservation_data.slot_time.time()
        <= operating_hours.closing_time
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Slot time {reservation_data.slot_time} is outside the operating hours "
                f"({operating_hours.opening_time} - {operating_hours.closing_time})"
            ),
        )

    # Prevent scheduling duplicate slots (apart from the current one)
    existing_slot = (
        db.query(ReservationSlot)
        .filter(
            ReservationSlot.restaurant_id == restaurant_id,
            ReservationSlot.slot_time == reservation_data.slot_time,
            ReservationSlot.slot_id != slot_id,
        )
        .first()
    )
    if existing_slot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A slot at this time already exists for the restaurant",
        )

    # Update slot fields
    slot.slot_time = reservation_data.slot_time
    slot.available_tables = reservation_data.available_tables
    slot.is_active = reservation_data.is_active

    db.commit()
    db.refresh(slot)

    return slot


@router.delete(
    "/restaurants/{restaurant_id}/slots/{slot_id}",
    summary="Deactivate a reservation slot",
)
async def delete_reservation_slot(
    restaurant_id: int, slot_id: int, request: Request, db: Session = Depends(get_db)
):
    # Verify the user's role
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete reservation slots",
        )

    # Confirm that the restaurant exists
    restaurant = (
        db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
        )

    # Retrieve the reservation slot to be deleted/deactivated
    slot = (
        db.query(ReservationSlot)
        .filter(
            ReservationSlot.restaurant_id == restaurant_id,
            ReservationSlot.slot_id == slot_id,
        )
        .first()
    )
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation slot not found"
        )

    # Instead of performing a hard delete, deactivate the slot
    slot.is_active = False
    db.commit()

    # Return no content on successful deletion
    return {"message": "Reservation Slot deleted successfully"}
