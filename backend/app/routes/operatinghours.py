from datetime import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Request, logger
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RestaurantModel
from app.models.OperatingHoursModel import OperatingHours
from app.schemas import RestaurantSchema
from app.schemas.OperatingHoursSchema import OperatingHoursCreate, OperatingHoursBulkCreate

# Define the router
router = APIRouter()


def check_timeframes(start_1: time, end_1: time, start_2: time, end_2: time) -> bool:
    if start_1 is None and end_1 is None:
        return True
    # They overlap if the start of one interval is before the end of the other and vice versa.
    return end_1 <= start_2 or end_2 <= start_1


@router.post(
    "/manager/restaurants/{restaurant_id}/hours",
    response_model=List[RestaurantSchema.OperatingHoursResponse],
)
async def create_operating_hours(
    restaurant_id: int,
    operating_hours: OperatingHoursBulkCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    # Verify that the user is authorized to perform this action.
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to create operating hours"
        )

    # Verify that the restaurant exists.
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.restaurant_id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    created_hours = []
    for hours in operating_hours.operating_hours:
        # Check for existing hours for the same day
        existing_hours = (
            db.query(OperatingHours)
            .filter(
                OperatingHours.restaurant_id == restaurant_id,
                OperatingHours.day_of_week == hours.day_of_week,
            )
            .first()
        )

        # Check if the new operating hours conflict with existing ones for the same day of the week.
        if existing_hours:
            if not check_timeframes(
                hours.opening_time,
                hours.closing_time,
                existing_hours.opening_time,
                existing_hours.closing_time,
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Operating hours conflict: the specified time frame overlaps with an existing schedule for {hours.day_of_week}.",
                )

        # Create new operating hours record
        new_operating_hours = OperatingHours(
            day_of_week=hours.day_of_week,
            opening_time=hours.opening_time,
            closing_time=hours.closing_time,
            restaurant_id=restaurant_id,
        )
        db.add(new_operating_hours)
        created_hours.append(new_operating_hours)

    db.commit()
    
    # Refresh all created records
    for hours in created_hours:
        db.refresh(hours)

    if not created_hours:
        raise HTTPException(status_code=400, detail="Failed to create operating hours")

    return created_hours


@router.get(
    "/manager/restaurants/{restaurant_id}/hours",
    response_model=List[RestaurantSchema.OperatingHoursResponse],
)
async def get_operating_hours(
    restaurant_id: int, request: Request, db: Session = Depends(get_db)
):
    # Verify that the user is authorized to perform this action.
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to view operating hours"
        )

    # Verify that the restaurant exists.
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.restaurant_id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Fetch operating hours for the given restaurant ID
    operating_hours = (
        db.query(OperatingHours)
        .filter(OperatingHours.restaurant_id == restaurant_id)
        .all()
    )
    if not operating_hours:
        raise HTTPException(
            status_code=404, detail="No operating hours found for this restaurant"
        )

    return operating_hours


@router.put(
    "/manager/restaurants/{restaurant_id}/hours",
    response_model=List[RestaurantSchema.OperatingHoursResponse],
)
async def update_operating_hours(
    restaurant_id: int,
    operating_hours: OperatingHoursBulkCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    # Verify that the user is authorized to perform this action.
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to update operating hours"
        )

    # Verify that the restaurant exists.
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.restaurant_id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    updated_hours = []
    for hours in operating_hours.operating_hours:
        # Check for existing hours for the same day
        existing_hours = (
            db.query(OperatingHours)
            .filter(
                OperatingHours.restaurant_id == restaurant_id,
                OperatingHours.day_of_week == hours.day_of_week,
            )
            .first()
        )

        if existing_hours:
            # Update existing record
            existing_hours.opening_time = hours.opening_time
            existing_hours.closing_time = hours.closing_time
            updated_hours.append(existing_hours)
        else:
            # Create new record if it doesn't exist
            new_operating_hours = OperatingHours(
                day_of_week=hours.day_of_week,
                opening_time=hours.opening_time,
                closing_time=hours.closing_time,
                restaurant_id=restaurant_id,
            )
            db.add(new_operating_hours)
            updated_hours.append(new_operating_hours)

    db.commit()
    
    # Refresh all updated records
    for hours in updated_hours:
        db.refresh(hours)

    if not updated_hours:
        raise HTTPException(status_code=400, detail="Failed to update operating hours")

    return updated_hours


@router.delete(
    "/manager/restaurants/{restaurant_id}/hours/{hours_id}", response_model=dict
)
async def delete_operating_hours(
    restaurant_id: int, hours_id: int, request: Request, db: Session = Depends(get_db)
):
    # Verify that the user is authorized to perform this action.
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to delete operating hours"
        )

    # Verify that the restaurant exists.
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.restaurant_id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Fetch the existing operating hours record
    operating_hours = (
        db.query(OperatingHours)
        .filter(
            OperatingHours.hours_id == hours_id,
            OperatingHours.restaurant_id == restaurant_id,
        )
        .first()
    )
    if not operating_hours:
        raise HTTPException(status_code=404, detail="Operating hours not found")

    # Delete the record
    db.delete(operating_hours)
    db.commit()
    return {"message": "Operating hours deleted successfully"}
