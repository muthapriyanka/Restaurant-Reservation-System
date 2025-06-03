import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import RestaurantList from "./RestaurantList";
import { getAllAdminRestaurants } from "./api/auth";
import Header from "./Header";

const dummyRestaurants = [
  {
    restaurant_id: 1,
    name: "The Fancy Fork",
    description: "A fine dining experience with international cuisine.",
    city: "San Francisco",
    state: "CA",
    email: "contact@fancyfork.com",
    phone_number: "(415) 123-4567",
  },
  {
    restaurant_id: 2,
    name: "Burger Bunker",
    description: "Casual joint serving gourmet burgers and craft beer.",
    city: "Austin",
    state: "TX",
    email: "info@burgerbunker.com",
    phone_number: "(512) 987-6543",
  },
  {
    restaurant_id: 3,
    name: "Pasta Palace",
    description: "Homemade pasta and traditional Italian dishes.",
    city: "Chicago",
    state: "IL",
    email: "reservations@pastapalace.com",
    phone_number: "(312) 555-9012",
  },
  {
    restaurant_id: 4,
    name: "Sushi Zen",
    description: "Authentic Japanese sushi and sashimi.",
    city: "Seattle",
    state: "WA",
    email: "hello@sushizen.com",
    phone_number: "(206) 111-2222",
  },
  {
    restaurant_id: 5,
    name: "Taco Town",
    description: "Street-style tacos and fresh margaritas.",
    city: "Los Angeles",
    state: "CA",
    email: "info@tacotown.com",
    phone_number: "(323) 789-1234",
  },
  {
    restaurant_id: 6,
    name: "Curry Corner",
    description: "Spicy and savory Indian curries made from scratch.",
    city: "New York",
    state: "NY",
    email: "support@currycorner.com",
    phone_number: "(212) 456-7890",
  },
  {
    restaurant_id: 7,
    name: "The Green Spoon",
    description: "Vegetarian and vegan meals with local ingredients.",
    city: "Portland",
    state: "OR",
    email: "hello@greenspoon.com",
    phone_number: "(503) 234-8765",
  },
  {
    restaurant_id: 8,
    name: "Bistro Bella",
    description: "Romantic European bistro with candlelit ambiance.",
    city: "Boston",
    state: "MA",
    email: "book@bistrobella.com",
    phone_number: "(617) 321-4567",
  },
  {
    restaurant_id: 9,
    name: "Pizza Planet",
    description: "Wood-fired pizzas with galactic flavors.",
    city: "Orlando",
    state: "FL",
    email: "orders@pizzaplanet.com",
    phone_number: "(407) 111-3344",
  },
  {
    restaurant_id: 10,
    name: "Grill & Chill",
    description: "Backyard-style grilled meats and craft drinks.",
    city: "Denver",
    state: "CO",
    email: "grill@chill.com",
    phone_number: "(303) 222-9090",
  },
];

const AdminDashboard = () => {
  const navigate = useNavigate();
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

  const handleGoto = () => {
    navigate("/adminAnalytics");
  };

  return (
    <>
     <Header />
      <div class="admin-dashboard-bg">
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
