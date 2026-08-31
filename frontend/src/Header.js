import React from "react";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("role");
    navigate("/login");
  };

  const shouldShowAnalytics = () => {
    return localStorage.getItem("role") === "ADMIN";
  };

  const shouldShowMyBookings = () => {
    return localStorage.getItem("role") === "CUSTOMER";
  };

  return (
    <div className="app-header-actions">
      {shouldShowAnalytics() ? (
        <button
          className="logout-fixed-btn"
          onClick={() => navigate("/adminAnalytics")}
        >
          Admin Analytics
        </button>
      ) : (
        ""
      )}

      {shouldShowMyBookings() ? (
        <button
          className="logout-fixed-btn"
          onClick={() => navigate("/my-bookings")}
        >
          My Bookings
        </button>
      ) : (
        ""
      )}

      <button className="logout-fixed-btn" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
};

export default Header;
