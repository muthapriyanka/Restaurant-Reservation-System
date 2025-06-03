# app/routers/photos.py

from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from sqlalchemy.orm import Session

from app import database
from app.models import RestaurantModel, RestaurantManagerModel, PhotoModel
from app.schemas.PhotoSchema import (
    RestaurantPhotoCreate,
    RestaurantPhotoUpdate,
    RestaurantPhotoResponse,
)

router = APIRouter()


def _verify_manager_and_restaurant(
    restaurant_id: int, user: dict, db: Session
) -> RestaurantModel.Restaurant:
    # Role check
    if user.get("role") != "restaurant_manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to manage photos",
        )

    # Find manager record
    manager = (
        db.query(RestaurantManagerModel.RestaurantManager)
        .filter(RestaurantManagerModel.RestaurantManager.user_id == user.get("user_id"))
        .first()
    )
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager record not found",
        )

    # Ensure restaurant belongs to this manager
    restaurant = (
        db.query(RestaurantModel.Restaurant)
        .filter_by(
            restaurant_id=restaurant_id,
            manager_id=manager.manager_id,
        )
        .first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found or not managed by you",
        )
    return restaurant


@router.get(
    "/manager/restaurants/{restaurant_id}/photos",
    response_model=List[RestaurantPhotoResponse],
)
async def list_photos(
    restaurant_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    _verify_manager_and_restaurant(restaurant_id, user, db)

    photos = (
        db.query(PhotoModel.RestaurantPhoto)
        .filter_by(restaurant_id=restaurant_id)
        .order_by(PhotoModel.RestaurantPhoto.display_order)
        .all()
    )
    return photos


@router.post(
    "/manager/restaurants/{restaurant_id}/photos",
    response_model=RestaurantPhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_photo(
    restaurant_id: int,
    photo_in: RestaurantPhotoCreate,
    request: Request,
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    _verify_manager_and_restaurant(restaurant_id, user, db)

    db_photo = PhotoModel.RestaurantPhoto(
        restaurant_id=restaurant_id,
        **photo_in.dict(),
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


@router.put(
    "/manager/restaurants/{restaurant_id}/photos/{photo_id}",
    response_model=RestaurantPhotoResponse,
)
async def update_photo(
    restaurant_id: int,
    photo_id: int,
    photo_upd: RestaurantPhotoUpdate,
    request: Request,
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    _verify_manager_and_restaurant(restaurant_id, user, db)

    photo = (
        db.query(PhotoModel.RestaurantPhoto)
        .filter_by(photo_id=photo_id, restaurant_id=restaurant_id)
        .first()
    )
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found",
        )

    # Update only provided fields
    update_data = photo_upd.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(photo, field, value)

    db.commit()
    db.refresh(photo)
    return photo


@router.delete(
    "/manager/restaurants/{restaurant_id}/photos/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_photo(
    restaurant_id: int,
    photo_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    _verify_manager_and_restaurant(restaurant_id, user, db)

    photo = (
        db.query(PhotoModel.RestaurantPhoto)
        .filter_by(photo_id=photo_id, restaurant_id=restaurant_id)
        .first()
    )
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found",
        )

    db.delete(photo)
    db.commit()
    # 204 No Content
