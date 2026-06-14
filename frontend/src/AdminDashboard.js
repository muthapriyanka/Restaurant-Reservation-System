import React, { useEffect, useState } from "react";
import RestaurantList from "./RestaurantList";
import { getAllAdminRestaurants } from "./api/auth";
import Header from "./Header";

const AdminDashboard = () => {
  const [pendingRestaurants, setPendingRestaurants] = useState([]);
  const [approvedRestaurants, setApprovedRestaurants] = useState([]);
  const fetchData = async () => {
    try {
      const res = await getAllAdminRestaurants();
      setApprovedRestaurants(
        res.filter((restaurant) => restaurant.is_approved)
      ); // store in state if needed
      setPendingRestaurants(
        res.filter((restaurant) => !restaurant.is_approved)
      );
    } catch (err) {
      console.error("Error fetching admin restaurants:", err);
    }
  };
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
     <Header />
      <div className="admin-dashboard-bg">
        <div className="admin-dashboard-overlay">
          <div className="admin-dashboard-content">
            <h1 className="textCenter">Admin Dashboard</h1>
            <div>
              <RestaurantList
                restaurants={pendingRestaurants}
                isNavigationFromAdmin={true}
                refreshData={fetchData}
              />
            </div>

            <h2 className="textCenter">Existing Restaurants</h2>
            <div>
              <RestaurantList
                restaurants={approvedRestaurants}
                isNavigationFromAdmin={true}
                isRemoveRestaurant={true}
                refreshData={fetchData}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default AdminDashboard;
