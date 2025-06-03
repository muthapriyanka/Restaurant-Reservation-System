import React from "react";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
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
    <>
      {shouldShowAnalytics() ? (
        <button
          className="logout-fixed-btn logout-fixed-wrapper"
          onClick={() => navigate("/adminAnalytics")}
          style={{ marginRight: "7%", width: "20%" }}
        >
          Admin Analytics
        </button>
      ) : (
        ""
      )}

      {shouldShowMyBookings() ? (
        <button
          className="logout-fixed-btn logout-fixed-wrapper"
          onClick={() => navigate("/my-bookings")}
          style={{ marginRight: "7%", width: "9%" }}
        >
          My Bookings
        </button>
      ) : (
        ""
      )}

      <div className="logout-fixed-wrapper">
        <button className="logout-fixed-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </>
  );
};

export default Header;
