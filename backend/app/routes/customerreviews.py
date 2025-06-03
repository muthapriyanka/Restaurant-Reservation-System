from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.CustomerModel import Customer
from app.models.CustomerReviewModel import Review
from app.models.RestaurantModel import Restaurant
from app.schemas.CustomerReviewSchema import (
    ReviewBase,
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
)

router = APIRouter()


@router.post("/restaurants/{restaurant_id}/reviews", response_model=ReviewResponse)
async def add_restaurant_review(
    restaurant_id: int,
    review_data: ReviewBase,
    request: Request,
    db: Session = Depends(get_db),
):
    # Check that the user has a customer role.
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Not authorized to create reviews")

    # Retrieve the customer record based on the authenticated user's id.
    customer = db.query(Customer).filter(Customer.user_id == user["user_id"]).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Verify the restaurant exists.
    restaurant = (
        db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Check if the customer already has a review for this restaurant.
    existing_review = (
        db.query(Review)
        .filter(
            Review.restaurant_id == restaurant_id,
            Review.customer_id == customer.customer_id,
        )
        .first()
    )
    if existing_review:
        raise HTTPException(
            status_code=400, detail="You have already reviewed this restaurant"
        )

    # Create the review.
    new_review = Review(
        customer_id=customer.customer_id,
        restaurant_id=restaurant_id,
        rating=review_data.rating,
        comment=review_data.comment,
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    # Calculate new average rating
    all_reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    total_rating = sum(review.rating for review in all_reviews)
    avg_rating = total_rating / len(all_reviews)

    # Update restaurant's average rating
    restaurant.avg_rating = avg_rating
    db.commit()
    db.refresh(restaurant)  # Refresh the restaurant object

    return new_review


@router.get(
    "/restaurants/{restaurant_id}/reviews",
    response_model=List[ReviewResponse],
    tags=["Reviews"],
)
async def get_restaurant_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    # Verify that the restaurant exists.
    restaurant = (
        db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    )
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Retrieve all reviews for the given restaurant.
    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    return reviews


# PUT /api/restaurants/reviews/{review_id} - Update a review.
@router.put(
    "/restaurants/reviews/{review_id}", response_model=ReviewResponse, tags=["Reviews"]
)
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    # Check that the user is a customer.
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Not authorized to update reviews")

    # Retrieve the review by review_id.
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Retrieve the customer record for the authenticated user.
    customer = db.query(Customer).filter(Customer.user_id == user["user_id"]).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Ensure the review belongs to the authenticated customer.
    if review.customer_id != customer.customer_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this review"
        )

    # Update review fields if provided in the payload.
    if review_update.rating is not None:
        review.rating = review_update.rating
    if review_update.comment is not None:
        review.comment = review_update.comment

    db.commit()
    db.refresh(review)

    # Calculate new average rating after update
    all_reviews = db.query(Review).filter(Review.restaurant_id == review.restaurant_id).all()
    total_rating = sum(review.rating for review in all_reviews)
    avg_rating = total_rating / len(all_reviews)

    # Update restaurant's average rating
    restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == review.restaurant_id).first()
    restaurant.avg_rating = avg_rating
    db.commit()
    db.refresh(restaurant)  # Refresh the restaurant object

    return review


# DELETE /api/restaurants/reviews/{review_id} - Delete a review.
@router.delete("/restaurants/reviews/{review_id}")
async def delete_review(
    review_id: int, request: Request, db: Session = Depends(get_db)
):
    # Check that the user is a customer.
    user = request.state.user
    if user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Not authorized to delete reviews")

    # Retrieve the review by review_id.
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Retrieve the customer record for the authenticated user.
    customer = db.query(Customer).filter(Customer.user_id == user["user_id"]).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Check if the authenticated customer is the owner of the review.
    if review.customer_id != customer.customer_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this review"
        )

    db.delete(review)
    db.commit()
    return {"detail": "Review deleted successfully"}
