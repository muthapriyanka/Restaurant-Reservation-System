import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { adminApproveRestaurant, adminRemoveRestaurant } from "./api/auth";
import "./styles.css";

const RestaurantList = ({
  restaurants,
  isNavigationFromAdmin,
  isRemoveRestaurant,
  refreshData,
}) => {
  const navigate = useNavigate();

  const handleUpdateClick = (restaurantId) => {
    navigate(`/update/${restaurantId}`);
  };

  const handleApproveClick = async (restaurantId) => {
    await adminApproveRestaurant({ restaurantId });
    if (refreshData) refreshData();
  };

  const handleRemoveClick = async (restaurantId) => {
    await adminRemoveRestaurant({ restaurantId });
    if (refreshData) refreshData();
  };

  return (
    <div className="list-container">
      <h2 className="page-title">
        {isNavigationFromAdmin
          ? isRemoveRestaurant
            ? "🗑️ Remove Restaurants"
            : "🛠️ Approve Restaurants"
          : "🍽️ Restaurant Directory"}
      </h2>
      <div className="card-grid">
        {restaurants.map((restaurant) => (
          <div key={restaurant.restaurant_id} className="restaurant-card">
            <h3 className="restaurant-name">{restaurant.name}</h3>
            <p className="description">{restaurant.description}</p>
            <p className="location">
              {restaurant.city}, {restaurant.state}
            </p>
            <p className="contact">
              {restaurant.email} | {restaurant.phone_number}
            </p>

            {isNavigationFromAdmin ? (
              isRemoveRestaurant ? (
                <button
                  className="remove-button"
                  onClick={() => handleRemoveClick(restaurant.restaurant_id)}
                >
                  ❌ Remove Restaurant
                </button>
              ) : (
                <>
                  <div
                    style={{ display: "flex", gap: "10px", marginTop: "10px" }}
                  >
                    <button
                      className="approve-button"
                      onClick={() =>
                        handleApproveClick(restaurant.restaurant_id)
                      }
                    >
                      ✅ Approve
                    </button>
                    <button
                      className="reject-button"
                      onClick={() =>
                        handleRemoveClick(restaurant.restaurant_id)
                      }
                    >
                      ❌ Reject
                    </button>
                  </div>
                </>
              )
            ) : (
              <>
                <p>
                  <Link
                    to={`/restaurant-details?restaurant_id=${restaurant.restaurant_id}`}
                    className="review-link"
                  >
                    📖 Restaurant Details
                  </Link>
                </p>
                <button
                  className="update-button"
                  onClick={() => handleUpdateClick(restaurant.restaurant_id)}
                >
                  ✏️ Update
                </button>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default RestaurantList;
