import React, { useEffect, useState } from "react";
import Header from "./Header";
import { addReview, cancelCustomerBooking, getAllBookings } from "./api/auth";

const CustomerBookings = () => {
  const [reservations, setReservations] = useState([]);
  const [selected, setSelected] = useState(null);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getAllBookings();
        setReservations(res);
      } catch (err) {
        console.error("Error fetching bookings for customer:", err);
      }
    };
    fetchData();
  }, []);

  const handleReviewSubmit = async () => {
    try {
      await addReview({
        restaurant_id: selected.restaurant_id,
        rating: parseInt(rating, 10),
        comment: comment.trim(),
      });
      alert("Review submitted successfully!");
      setSelected(null);
    } catch (err) {
      console.error("Error submitting review:", err);
    }
  };

  const handleCancel = async (reservation_id) => {
    try {
      await cancelCustomerBooking({ reservation_id });
      alert("Booking canceled");
      // // remove from UI or refetch:
      // setReservations((res) =>
      //   res.filter((r) => r.reservation_id !== reservation_id)
      // );
    } catch (err) {
      console.error("Error cancelling:", err);
    }
  };

  return (
    <>
      <Header />
      <div className="customer-bookings">
        <div className="customer-bookings-content">
          <h2>My Bookings</h2>
          {reservations.length === 0 ? (
            <p>No reservations found.</p>
          ) : (
            reservations.map((res) => (
              <div key={res.reservation_id} className="result-card">
                <h3>Reservation #{res.reservation_id}</h3>
                <p>
                  <strong>Restaurant ID:</strong> {res.restaurant_id}
                </p>
                <p>
                  <strong>Restaurant name:</strong> {res.restaurant_name}
                </p>
                <p>
                  <strong>Party Size:</strong> {res.party_size}
                </p>
                <p>
                  <strong>Time:</strong>{" "}
                  {new Date(res.reservation_time).toLocaleString()}
                </p>
                <p>
                  <strong>Status:</strong> {res.status}
                </p>
                <p>
                  <strong>Table ID:</strong> {res.table_id}
                </p>
                <p>
                  <strong>Confirmation Code:</strong> {res.confirmation_code}
                </p>
                {res.special_requests && (
                  <p>
                    <strong>Special Requests:</strong> {res.special_requests}
                  </p>
                )}

                {res.status.toLowerCase() === "completed" && (
                  <button
                    onClick={() => setSelected(res)}
                    className="review-button"
                  >
                    Leave a Review
                  </button>
                )}

                {res.status.toLowerCase() === "confirmed" && (
                  <button
                    onClick={() => handleCancel(res.reservation_id)}
                    className="cancel-button"
                  >
                    Cancel Booking
                  </button>
                )}
              </div>
            ))
          )}

          {selected && (
            <div className="review-modal">
              <h3>Review for Reservation #{selected.reservation_id}</h3>
              <label>
                Rating:
                <select
                  className="review-rating-select"
                  value={rating}
                  onChange={(e) => setRating(e.target.value)}
                  style={{ marginLeft: "10px", color: "black" }}
                >
                  {[5, 4, 3, 2, 1].map((r) => (
                    <option key={r} value={r}>
                      {r}
                    </option>
                  ))}
                </select>
              </label>
              <br />
              <textarea
                className="special-request-textarea"
                rows={4}
                placeholder="Write your review..."
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                style={{ marginTop: "10px", width: "100%" }}
              />
              <br />
              <button
                onClick={handleReviewSubmit}
                className="submit-review-btn"
              >
                Submit Review
              </button>
              <button
                onClick={() => setSelected(null)}
                className="cancel-review-btn"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default CustomerBookings;
