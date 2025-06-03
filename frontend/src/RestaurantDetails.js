import React, { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { getRestaurantDetailForManager } from "./api/auth";
import Header from "./Header";
import "./RestaurantDetails.css";

const capitalize = (s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : "");
const formatCost = (n) => "$".repeat(n || 0);

const RestaurantDetails = () => {
  const [searchParams] = useSearchParams();
  const restaurantId = searchParams.get("restaurant_id");
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!restaurantId) {
      setError("No restaurant ID provided.");
      setLoading(false);
      return;
    }
    (async () => {
      try {
        const data = await getRestaurantDetailForManager({ id: restaurantId });
        setRestaurant(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load restaurant details.");
      } finally {
        setLoading(false);
      }
    })();
  }, [restaurantId]);

  if (loading) return <div className="loading">Loading…</div>;
  if (error) return <div className="error">{error}</div>;

  const {
    name,
    description,
    address_line1,
    address_line2,
    city,
    state,
    zip_code,
    phone_number,
    email,
    cuisine_type,
    cost_rating,
    avg_rating,
    photos = [],
    operating_hours = [],
    availability = [],
  } = restaurant;

  return (
    <>
      <Header />
      <div className="read-reviews-bg">
        <div className="read-reviews-container">
          <h2>🏠 Restaurant Details</h2>

          {/* Name & Description */}
          <div className="review-card">
            <h3 className="card-title">{name}</h3>
            <p className="description">{description}</p>
          </div>

          {/* Address */}
          <div className="review-card">
            <h3 className="card-title">Address</h3>
            <p>
              {address_line1}
              {address_line2 && `, ${address_line2}`}
            </p>
            <p>
              {city}, {state} {zip_code}
            </p>
          </div>

          {/* Contact */}
          <div className="review-card">
            <h3 className="card-title">Contact</h3>
            <p>📞 {phone_number}</p>
            <p>✉️ {email}</p>
          </div>

          {/* Details */}
          <div className="review-card">
            <h3 className="card-title">Details</h3>
            <p>
              <strong>Cuisine:</strong> {capitalize(cuisine_type)}
            </p>
            <p>
              <strong>Cost:</strong> {formatCost(cost_rating)}
            </p>
            <p>
              <strong>Average Rating:</strong> {avg_rating?.toFixed(1) ?? "N/A"}
            </p>
          </div>

          {/* Photos */}
          {photos.length > 0 && (
            <div className="review-card">
              <h3 className="card-title">Photos</h3>
              <div className="photos-grid">
                {photos.map((url, i) => (
                  <img
                    key={i}
                    src={url}
                    alt={`${name} photo ${i + 1}`}
                    className="restaurant-photo"
                  />
                ))}
              </div>
            </div>
          )}

          {/* Operating Hours */}
          {operating_hours.length > 0 && (
            <div className="review-card">
              <h3 className="card-title">Operating Hours</h3>
              <ul className="hours-list">
                {operating_hours.map((h, idx) => (
                  <li key={idx}>
                    {capitalize(h.day_of_week)}: {h.opening_time.slice(0, 5)} –{" "}
                    {h.closing_time.slice(0, 5)}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Available Slots */}
          {availability.length > 0 && (
            <div className="review-card">
              <h3 className="card-title">Available Slots</h3>
              <div className="slots-badges">
                {availability.map((slot) => (
                  <span key={slot} className="slot-badge">
                    {slot}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Read Reviews Link */}
          <div className="review-card">
            <Link
              to={`/read-review?restaurant_id=${restaurantId}`}
              className="review-link"
            >
              📖 Read Reviews
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default RestaurantDetails;
