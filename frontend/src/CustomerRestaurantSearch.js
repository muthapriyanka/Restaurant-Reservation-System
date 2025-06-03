import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Header from "./Header";
import { getAllRestaurantsForCustomers } from "./api/auth";

const CustomerRestaurantSearch = () => {
  const [filters, setFilters] = useState({
    date: "",
    time: "",
    people: "",
    location: "",
  });

  const navigate = useNavigate();
  const [restaurants, setRestaurants] = useState([]);
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        const data = await getAllRestaurantsForCustomers();
        setRestaurants(data);
        setResults(data);
      } catch (error) {
        console.error("Failed to fetch restaurants:", error);
      }
    };
    fetchRestaurants();
  }, []);

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const generateTimeOptions = () => {
    const times = [];
    for (let hour = 0; hour < 24; hour++) {
      for (let min = 0; min < 60; min += 30) {
        const formatted = `${String(hour).padStart(2, "0")}:${String(
          min
        ).padStart(2, "0")}`;
        times.push(formatted);
      }
    }
    return times;
  };

  const getNearbyTimes = (timeStr) => {
    const [h, m] = timeStr.split(":").map(Number);
    const base = new Date(0, 0, 0, h, m);

    const offsets = [-30, 0, 30];
    return offsets.map((offset) => {
      const t = new Date(base.getTime() + offset * 60000);
      return `${String(t.getHours()).padStart(2, "0")}:${String(
        t.getMinutes()
      ).padStart(2, "0")}`;
    });
  };

  const handleSearch = () => {
    if (!filters.date || !filters.time) {
      alert("Please select a date and time.");
      return;
    }
    if (!filters.people || filters.people <= 0) {
      alert("Please enter a valid number of people.");
      return;
    }

    const now = new Date();
    const nearbyTimes = getNearbyTimes(filters.time);
    const nearbyDateTimes = nearbyTimes.map(
      (timeStr) => new Date(`${filters.date}T${timeStr}`)
    );
    const anyFutureSlot = nearbyDateTimes.some((dt) => dt > now);

    if (!anyFutureSlot) {
      alert("Date not available. Please select a future time.");
      return;
    }

    const filtered = restaurants.filter((r) => {
      const matchesLocation =
        !filters.location ||
        r.city.toLowerCase().includes(filters.location.toLowerCase()) ||
        r.state.toLowerCase().includes(filters.location.toLowerCase()) ||
        r.zip_code.includes(filters.location);

      // const hasAvailableSlot = r.availability?.some(
      //   (slot) => nearbyTimes.includes(slot) && !r.booked_slots?.includes(slot)
      // );
      const hasAvailableSlot =
        r.availability?.some((slot) => nearbyTimes.includes(slot)) &&
        r.tables.some((t) => t.is_active === true);
      return matchesLocation && hasAvailableSlot;
    });

    setResults(filtered);
    setHasSearched(true);
  };

  const handleBooking = (restaurant, time) => {
    navigate(
      `/book/${restaurant.restaurant_id}?time=${time}&date=${filters.date}&people=${filters.people}`
    );
  };

  return (
    <>
      <Header />
      <div className="customer-bg">
        <div className="customer-search-container">
          <h2>Find a Restaurant</h2>

          <div className="filters">
            <input
              type="date"
              name="date"
              value={filters.date}
              onChange={handleChange}
            />
            <select
              className="filtersSelect"
              name="time"
              value={filters.time}
              onChange={handleChange}
            >
              <option value="">Select Time</option>
              {generateTimeOptions().map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
            <input
              type="number"
              name="people"
              placeholder="# People"
              value={filters.people}
              onChange={handleChange}
            />
            <input
              type="text"
              name="location"
              placeholder="City / State / Zip (optional)"
              value={filters.location}
              onChange={handleChange}
            />
            <button onClick={handleSearch}>Search</button>
          </div>

          <div className="results">
            {results.length === 0 ? (
              <p>No restaurants match your search.</p>
            ) : (
              results.map((r) => (
                <div key={r.restaurant_id} className="result-card">
                  <h3>{r.name}</h3>
                  <p>
                    Cuisine: <strong>{r.cuisine_type}</strong> | Cost: {""}
                    <strong>{"$".repeat(r.cost_rating)}</strong>
                  </p>
                  <p>
                    {r.avg_rating} ⭐ ({r.reviews.length} reviews) | Booked {""}
                    {r.times_booked_today} times today
                  </p>
                  <p>
                    <Link
                      to={`/read-review?restaurant_id=${r.restaurant_id}`}
                      className="review-link"
                    >
                      📖 Read Reviews
                    </Link>
                  </p>
                  <p>
                    <Link
                      to={`/restaurant-details?restaurant_id=${r.restaurant_id}`}
                      className="review-link"
                    >
                      📖 Restaurant Details
                    </Link>
                  </p>

                  {hasSearched && filters.time && (
                    <div className="slots">
                      {r.availability
                        ?.filter(
                          (slot) =>
                            getNearbyTimes(filters.time).includes(slot) &&
                            !r.booked_slots?.includes(slot)
                        )
                        .map((slot) => (
                          <button
                            key={slot}
                            onClick={() => handleBooking(r, slot)}
                            className="slot-btn"
                          >
                            {slot}
                          </button>
                        ))}
                      {r.availability?.filter(
                        (slot) =>
                          getNearbyTimes(filters.time).includes(slot) &&
                          !r.booked_slots?.includes(slot)
                      ).length === 0 && (
                        <p style={{ color: "#ccc", marginTop: "8px" }}>
                          No available slots near this time.
                        </p>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default CustomerRestaurantSearch;
