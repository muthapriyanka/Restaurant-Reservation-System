import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import RestaurantList from "./RestaurantList";
import { getAllRestaurantsForManager } from "./api/auth";
import "./styles.css";
import Header from "./Header";

const ManagerDashboard = () => {
  const [restaurants, setRestaurants] = useState([]);
  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      const res = await getAllRestaurantsForManager();
      setRestaurants(res);
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
    <div className="manager-dashboard-bg">
      <div className="dashboard-content">
        <h1 className="textCenter">Manager Dashboard</h1>

        <div className="textCenter paddingBottom5">
          <button
            className="addNewRestaurantBtn"
            onClick={() => navigate("/addRestaurantForm")}
          >
            Add New Restaurant
          </button>
        </div>
        <div>
          <RestaurantList restaurants={restaurants} />
        </div>
      </div>
    </div>
    </>
  );
};

export default ManagerDashboard;
