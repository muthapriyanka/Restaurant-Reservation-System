from datetime import datetime, date as dt_date, time as dt_time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import Table, func, or_

from app import database
from app.models import RestaurantManagerModel, RestaurantModel, TableModel
from app.models import ReservationSlotModel, OperatingHoursModel
from app.schemas import RestaurantSchema

from app.models.RestaurantModel import Restaurant
from app.models.TableModel import Table
from app.models.ReservationSlotModel import ReservationSlot

router = APIRouter()


# Manager routes for restaurant management
@router.post("/manager/restaurants", response_model=RestaurantSchema.RestaurantResponse)
async def create_restaurant(
    restaurant: RestaurantSchema.RestaurantCreate,
    request: Request,
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to create a restaurant"
        )

    manager = (
        db.query(RestaurantManagerModel.RestaurantManager)
        .filter(RestaurantManagerModel.RestaurantManager.user_id == user["user_id"])
        .first()
    )
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    db_restaurant = RestaurantModel.Restaurant(
        manager_id=manager.manager_id,
        name=restaurant.name,
        description=restaurant.description,
        address_line1=restaurant.address_line1,
        address_line2=restaurant.address_line2,
        city=restaurant.city,
        state=restaurant.state,
        zip_code=restaurant.zip_code,
        phone_number=restaurant.phone_number,
        email=restaurant.email,
        cuisine_type=restaurant.cuisine_type,
        cost_rating=restaurant.cost_rating,
        availability=restaurant.availability,
        booked_slots=restaurant.booked_slots,
    )

    # Add the new restaurant to the DB session, commit the transaction, and refresh to get any auto-generated fields.
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


@router.get(
    "/manager/restaurants", response_model=list[RestaurantSchema.RestaurantDetailResponse]
)
async def get_restaurants_by_manager(
    request: Request, db: Session = Depends(database.get_db)
):
    # Check user role
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to view these restaurants"
        )

    # Retrieve the manager's record by user_id
    manager = (
        db.query(RestaurantManagerModel.RestaurantManager)
        .filter(RestaurantManagerModel.RestaurantManager.user_id == user["user_id"])
        .first()
    )
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    # Inline query to fetch restaurants for the manager
    restaurants = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.manager_id == manager.manager_id)
        .all()
    )
    return restaurants


@router.get(
    "/manager/restaurants/{restaurant_id}",
    response_model=RestaurantSchema.RestaurantResponse,
)
async def get_restaurant_details(
    restaurant_id: int, request: Request, db: Session = Depends(database.get_db)
):
    # Check user role
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to view this restaurant"
        )

    # Inline join to fetch restaurant details only if the restaurant is managed by this user
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .join(RestaurantManagerModel.RestaurantManager)
        .filter(
            RestaurantModel.Restaurant.restaurant_id == restaurant_id,
            RestaurantManagerModel.RestaurantManager.user_id == user["user_id"],
        )
        .first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=404, detail="Restaurant not found or not managed by you"
        )
    return restaurant


@router.put(
    "/manager/restaurants/{restaurant_id}",
    response_model=RestaurantSchema.RestaurantResponse,
)
async def update_restaurant_details(
    restaurant_id: int,
    restaurant_update: RestaurantSchema.RestaurantUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # Check user role
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to update this restaurant"
        )

    # Verify if the restaurant belongs to the authenticated manager
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .join(RestaurantManagerModel.RestaurantManager)
        .filter(
            RestaurantModel.Restaurant.restaurant_id == restaurant_id,
            RestaurantManagerModel.RestaurantManager.user_id == user["user_id"],
        )
        .first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=404, detail="Restaurant not found or not managed by you"
        )

    # Update only provided fields
    update_data = restaurant_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(restaurant, key, value)

    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.delete("/manager/restaurants/{restaurant_id}", status_code=204)
async def delete_manager_restaurant(
    restaurant_id: int, request: Request, db: Session = Depends(database.get_db)
):
    # Check user role
    user = request.state.user
    if user["role"] != "restaurant_manager":
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this restaurant"
        )

    # Verify if the restaurant exists and is managed by the user
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .join(RestaurantManagerModel.RestaurantManager)
        .filter(
            RestaurantModel.Restaurant.restaurant_id == restaurant_id,
            RestaurantManagerModel.RestaurantManager.user_id == user["user_id"],
        )
        .first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=404, detail="Restaurant not found or not managed by you"
        )

    # Delete the restaurant and commit the transaction
    db.delete(restaurant)
    db.commit()
    return {"detail": "Restaurant deleted successfully"}


# Admin Endpoints


@router.get(
    "/admin/restaurants", response_model=list[RestaurantSchema.RestaurantResponse]
)
async def get_all_restaurants(request: Request, db: Session = Depends(database.get_db)):
    # Check user role for admin privileges
    user = request.state.user
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403, detail="Not authorized to view all restaurants"
        )

    # Inline query to retrieve all restaurants
    restaurants = db.query(RestaurantModel.Restaurant).all()
    return restaurants


@router.delete("/admin/restaurants/{restaurant_id}", status_code=204)
async def delete_restaurant_admin(
    restaurant_id: int, request: Request, db: Session = Depends(database.get_db)
):
    # Check admin access
    user = request.state.user
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403, detail="Not authorized to delete a restaurant"
        )

    # Inline query to find the restaurant by its ID
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.restaurant_id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Delete tables
    db.query(TableModel.Table).filter(
        TableModel.Table.restaurant_id == restaurant_id
    ).delete()
    
    # Delete operating hours
    db.query(OperatingHoursModel.OperatingHours).filter(
        OperatingHoursModel.OperatingHours.restaurant_id == restaurant_id
    ).delete()
    
    db.delete(restaurant)
    db.commit()
    return {"detail": "Restaurant deleted successfully"}


@router.get(
    "/admin/restaurants/pending",
    response_model=List[RestaurantSchema.RestaurantResponse],
)
async def get_pending_restaurants(
    request: Request,
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view pending approvals",
        )

    pending = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.is_approved == False)
        .all()
    )
    return pending


@router.put(
    "/admin/restaurants/{restaurant_id}/approve",
    response_model=RestaurantSchema.RestaurantResponse,
)
async def approve_restaurant(
    restaurant_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to approve restaurants",
        )

    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.restaurant_id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    restaurant.is_approved = True
    restaurant.approved_at = datetime.utcnow()
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.put(
    "/admin/restaurants/{restaurant_id}/reject",
    response_model=RestaurantSchema.RestaurantResponse,
)
async def reject_restaurant(
    restaurant_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to reject restaurants",
        )

    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter(RestaurantModel.Restaurant.restaurant_id == restaurant_id)
        .first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    restaurant.is_approved = False
    restaurant.approved_at = None
    db.commit()
    db.refresh(restaurant)
    return restaurant


# Customer Endpoints


@router.get(
    "/restaurants/search",
    response_model=List[RestaurantSchema.RestaurantResponse],
    summary="Search restaurants by date, time, party size & location",
)
def search_restaurants(
    request: Request,
    reservation_date: dt_date = Query(
        ..., description="Required reservation date (YYYY-MM-DD)"
    ),
    reservation_time: Optional[dt_time] = Query(
        None, description="Optional reservation time (HH:MM:SS)"
    ),
    party_size: Optional[int] = Query(
        None, gt=0, description="Optional number of guests"
    ),
    location: Optional[str] = Query(
        None, description="Optional location substring (e.g. city or neighborhood)"
    ),
    db: Session = Depends(database.get_db),
):
    # ensure this endpoint is hit by a customer
    user = request.state.user
    if user.get("role") != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to search restaurants",
        )

    q = db.query(Restaurant)

    # filter by location if provided
    if location:
        loc_filter = or_(
            Restaurant.address_line1.ilike(f"%{location}%"),
            Restaurant.address_line2.ilike(f"%{location}%"),
            Restaurant.city.ilike(f"%{location}%"),
            Restaurant.state.ilike(f"%{location}%"),
            Restaurant.zip_code.ilike(f"%{location}%"),
        )
        q = q.filter(loc_filter)

    # filter by table capacity if provided
    if party_size:
        q = q.join(Table, Restaurant.restaurant_id == Table.restaurant_id).filter(
            Table.capacity >= party_size
        )

    # filter by slot date (always) and time (if provided)
    q = q.join(
        ReservationSlot, Restaurant.restaurant_id == ReservationSlot.restaurant_id
    )
    if reservation_time:
        dt_full = datetime.combine(reservation_date, reservation_time)
        q = q.filter(ReservationSlot.slot_time == dt_full)
    else:
        q = q.filter(func.date(ReservationSlot.slot_time) == reservation_date)

    # ensure at least one table is available
    q = q.filter(ReservationSlot.available_tables >= 1)

    results = q.distinct().all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No restaurants found matching criteria",
        )

    return results


@router.get(
    "/restaurants/{restaurant_id}",
    response_model=RestaurantSchema.RestaurantDetailResponse,
    summary="Get detailed restaurant information",
)
def get_restaurant_detail(
    restaurant_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    # # ensure this endpoint is hit by a customer
    # user = request.state.user
    # if user.get("role") != "customer":
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to view restaurant details",
    #     )

    # fetch only approved restaurants
    restaurant = (
        db.query(Restaurant)
        .filter(
            Restaurant.restaurant_id == restaurant_id,
            Restaurant.is_approved == True,
        )
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    return restaurant

# @router.get(
#     "/customer/restaurants", response_model=list[RestaurantSchema.RestaurantResponse]
# )
# async def get_customer_restaurants(request: Request, db: Session = Depends(database.get_db)):
#     # Get all approved restaurants
#     restaurants = (
#         db.query(RestaurantModel.Restaurant)
#         .filter(RestaurantModel.Restaurant.is_approved == True)
#         .all()
#     )
#     return restaurants

@router.get(
    "/customer/restaurants", response_model=list[RestaurantSchema.RestaurantDetailResponse]
)
async def get_all_restaurants(request: Request, db: Session = Depends(database.get_db)):
    # Check user role for customer privileges
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(
            status_code=403, detail="Not authorized to view all restaurants"
        )

    # Inline query to retrieve all restaurants
    restaurants = db.query(RestaurantModel.Restaurant).all()
    return restaurants