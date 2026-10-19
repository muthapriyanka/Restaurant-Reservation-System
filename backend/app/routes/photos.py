import os
from io import BytesIO
from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from app import database
from app.models import RestaurantModel, RestaurantManagerModel, PhotoModel
from app.schemas.PhotoSchema import (
    RestaurantPhotoCreate,
    RestaurantPhotoUpdate,
    RestaurantPhotoResponse,
)
from app.services import s3_storage

router = APIRouter()

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
BUNDLED_ASSET_DIR = Path(__file__).resolve().parents[3] / "deployment" / "assets"


def _bundled_asset_path(object_key: str) -> Path | None:
    prefix = "app-assets/"
    if not object_key.startswith(prefix):
        return None

    filename = object_key.removeprefix(prefix)
    if not filename or "/" in filename or "\\" in filename:
        return None

    asset_path = BUNDLED_ASSET_DIR / filename
    return asset_path if asset_path.is_file() else None


def _matches_declared_image_type(contents: bytes, content_type: str) -> bool:
    if content_type == "image/jpeg":
        return contents.startswith(b"\xff\xd8\xff")
    if content_type == "image/png":
        return contents.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type == "image/webp":
        return (
            len(contents) >= 12
            and contents.startswith(b"RIFF")
            and contents[8:12] == b"WEBP"
        )
    return False


@router.get("/media/{object_key:path}")
def read_media(object_key: str):
    if not object_key or object_key.startswith("/") or ".." in Path(object_key).parts:
        raise HTTPException(status_code=400, detail="Invalid media key")
    if not object_key.startswith(("app-assets/", "restaurants/")):
        raise HTTPException(status_code=404, detail="Image not found")

    bundled_asset = _bundled_asset_path(object_key)
    if bundled_asset:
        return FileResponse(
            bundled_asset,
            headers={
                "Cache-Control": "public, max-age=86400",
                "X-Content-Type-Options": "nosniff",
            },
        )

    try:
        stored_object = s3_storage.get_object(object_key)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")
    except (s3_storage.StorageConfigurationError, s3_storage.StorageOperationError):
        raise HTTPException(status_code=503, detail="Image storage is unavailable")

    return StreamingResponse(
        stored_object["Body"].iter_chunks(chunk_size=64 * 1024),
        media_type=stored_object.get("ContentType", "application/octet-stream"),
        headers={
            "Cache-Control": "public, max-age=86400",
            "X-Content-Type-Options": "nosniff",
        },
    )


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


@router.post(
    "/manager/restaurants/{restaurant_id}/photos/upload",
    response_model=RestaurantPhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_photo(
    restaurant_id: int,
    request: Request,
    image: UploadFile = File(...),
    caption: str | None = Form(None),
    display_order: int = Form(0),
    db: Session = Depends(database.get_db),
):
    user = request.state.user
    _verify_manager_and_restaurant(restaurant_id, user, db)

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Only JPEG, PNG, and WebP images are supported",
        )

    max_size = int(os.getenv("MAX_IMAGE_SIZE_MB", "5")) * 1024 * 1024
    contents = await image.read(max_size + 1)
    await image.close()
    if not contents:
        raise HTTPException(status_code=400, detail="Image is empty")
    if not _matches_declared_image_type(contents, image.content_type):
        raise HTTPException(status_code=400, detail="File content is not a valid image")
    if len(contents) > max_size:
        raise HTTPException(
            status_code=413,
            detail="Image exceeds the configured size limit",
        )

    extension = ALLOWED_IMAGE_TYPES[image.content_type]
    object_key = f"restaurants/{restaurant_id}/{uuid4().hex}{extension}"
    try:
        s3_storage.upload_file(BytesIO(contents), object_key, image.content_type)
    except (s3_storage.StorageConfigurationError, s3_storage.StorageOperationError):
        raise HTTPException(status_code=503, detail="Image storage is unavailable")

    db_photo = PhotoModel.RestaurantPhoto(
        restaurant_id=restaurant_id,
        url=f"/api/media/{object_key}",
        object_key=object_key,
        caption=caption[:255] if caption else None,
        display_order=display_order,
    )
    db.add(db_photo)
    try:
        db.commit()
        db.refresh(db_photo)
    except Exception:
        db.rollback()
        try:
            s3_storage.delete_object(object_key)
        except s3_storage.StorageOperationError:
            pass
        raise
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

    object_key = photo.object_key
    db.delete(photo)
    db.commit()
    if object_key:
        try:
            s3_storage.delete_object(object_key)
        except (s3_storage.StorageConfigurationError, s3_storage.StorageOperationError):
            # The database operation already succeeded; bucket lifecycle can
            # clean up an object if S3 is temporarily unavailable.
            pass
