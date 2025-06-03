import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import Header from "./Header";
import { getAllReviewsForRestaurant } from "./api/auth";

const ReadReview = () => {
  const [searchParams] = useSearchParams();
  const restaurantId = searchParams.get("restaurant_id");
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const res = await getAllReviewsForRestaurant({ restaurantId });
        setReviews(res);
      } catch (error) {
        console.error("Failed to fetch reviews:", error);
      } finally {
        setLoading(false);
      }
    };

    if (restaurantId) {
      fetchReviews();
    }
  }, [restaurantId]);

  return (
    <>
      <Header />
      <div className="read-reviews-bg">
        <div className="read-reviews-container">
          <h2>📖 Customer Reviews</h2>
          {loading ? (
            <p>Loading reviews...</p>
          ) : reviews.length === 0 ? (
            <p>No reviews found for this restaurant.</p>
          ) : (
            reviews.map((review) => (
              <div key={review.review_id} className="review-card">
                <p>
                  <strong>⭐ Rating:</strong> {review.rating}
                </p>
                <p>
                  <strong>📝 Comment:</strong> {review.comment}
                </p>
                <p className="review-timestamp">
                  📅 Posted on: {new Date(review.created_at).toLocaleString()}
                </p>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
};

export default ReadReview;
