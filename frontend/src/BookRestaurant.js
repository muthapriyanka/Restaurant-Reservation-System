import React, { useEffect, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { bookReservation, getAllRestaurantsForCustomers } from "./api/auth";

function ensureSeconds(timestamp) {
  // If it’s in “YYYY-MM-DD HH:mm” form (length = 16), just tack on “:00”
  if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(timestamp)) {
    return timestamp + ":00";
  }
  // Otherwise assume it already has seconds (or leave it untouched)
  return timestamp;
}

const BookRestaurant = () => {
  const [specialRequest, setSpecialRequest] = useState("");
  const [restaurants, setRestaurants] = useState([]);
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const people = searchParams.get("people");
  const time = searchParams.get("time");
  const date = searchParams.get("date");

  function toIsoZ(str) {
    return str.trim().replace(" ", "T") + "Z";
  }

  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        const data = await getAllRestaurantsForCustomers();
        setRestaurants(data.find((r) => r.restaurant_id === parseInt(id)));
      } catch (error) {
        console.error("Failed to fetch restaurants:", error);
      }
    };
    fetchRestaurants();
  }, []);
  console.log("Restaurants data:", restaurants);
  const reviews_count = restaurants?.reviews?.length || 0;
  if (!restaurants) return <p>Restaurant not found.</p>;

  const handleBook = async () => {
    const dateAndSlot = ensureSeconds(`${date} ${time}`);
    try {
      await bookReservation({
        restaurant_id: restaurants.restaurant_id,
        table_id: restaurants.tables.find(
          (t) => t.capacity >= people && t.is_active === true
        ).table_id,
        reservation_time: toIsoZ(dateAndSlot),
        party_size: Number(people),
        special_requests: specialRequest,
      });
      alert(
        `✅ Table booked at ${restaurants.name} for ${time}. Confirmation sent!`
      );
      navigate("/my-bookings");
    } catch (err) {
      console.error("Error booking", err);
    }

    // In real app: send API request, email/SMS
  };

  const handleCancel = () => {
    navigate("/custDashboard");
  };

  return (
    <div className="book-bg">
      <div className="booking-container">
        <h2>Booking at {restaurants.name}</h2>
        <p>
          <strong>Time:</strong> {time}
        </p>
        <p>
          <strong>Date:</strong> {date}
        </p>
        <p>
          <strong>Party Size:</strong> {people}
        </p>
        <p>
          <strong>Cuisine:</strong> {restaurants.cuisine_type}
        </p>
        <p>
          <strong>Rating:</strong> {restaurants.avg_rating} ⭐ ({reviews_count}{" "}
          reviews)
        </p>

        <h4>📍 Location</h4>
        <a
          href={`https://www.google.com/maps/search/?api=1&query=${restaurants.name}+${restaurants.city}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          View on Google Maps
        </a>

        <h4>📝 Special Requests</h4>
        <textarea
          className="special-request-textarea"
          value={specialRequest}
          onChange={(e) => setSpecialRequest(e.target.value)}
          placeholder="E.g. Table near the window, vegetarian meal..."
          rows={4}
        />

        <h4>🪑 Booking Actions</h4>
        <button onClick={handleBook}>Book Table</button>
        <button onClick={handleCancel}>Discard Booking</button>
      </div>
    </div>
  );
};

export default BookRestaurant;
