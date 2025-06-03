import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import RestaurantList from "./RestaurantList";
import { getAllRestaurantsForManager } from "./api/auth";
import "./styles.css";
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
  {
    restaurant_id: 11,
    name: "Noodle Nest",
    description: "Asian noodle dishes from across the continent.",
    city: "Philadelphia",
    state: "PA",
    email: "hello@noodlenest.com",
    phone_number: "(215) 999-1234",
  },
  {
    restaurant_id: 12,
    name: "Smokehouse Station",
    description: "Smoked BBQ ribs, brisket, and southern sides.",
    city: "Nashville",
    state: "TN",
    email: "smoke@station.com",
    phone_number: "(615) 444-7777",
  },
  {
    restaurant_id: 13,
    name: "The Breakfast Club",
    description: "All-day breakfast with a modern twist.",
    city: "Phoenix",
    state: "AZ",
    email: "breakfast@club.com",
    phone_number: "(602) 123-1111",
  },
  {
    restaurant_id: 14,
    name: "Mediterraneo",
    description: "Greek, Turkish, and Lebanese fusion meals.",
    city: "Miami",
    state: "FL",
    email: "hello@mediterraneo.com",
    phone_number: "(305) 567-9876",
  },
  {
    restaurant_id: 15,
    name: "Urban Wok",
    description: "Fast-casual stir-fry bowls with global flavors.",
    city: "Minneapolis",
    state: "MN",
    email: "order@urbanwok.com",
    phone_number: "(612) 555-1212",
  },
  {
    restaurant_id: 16,
    name: "The Crab Shack",
    description: "Fresh seafood and crab boils by the shore.",
    city: "Charleston",
    state: "SC",
    email: "crab@shack.com",
    phone_number: "(843) 333-4567",
  },
  {
    restaurant_id: 17,
    name: "Pho Real",
    description: "Vietnamese pho, banh mi, and iced coffee.",
    city: "Houston",
    state: "TX",
    email: "pho@real.com",
    phone_number: "(713) 789-2222",
  },
  {
    restaurant_id: 18,
    name: "Zen Garden",
    description: "Peaceful atmosphere with Japanese vegetarian fare.",
    city: "San Diego",
    state: "CA",
    email: "garden@zen.com",
    phone_number: "(858) 123-4567",
  },
  {
    restaurant_id: 19,
    name: "BBQ Barn",
    description: "Rustic smokehouse with live country music.",
    city: "Dallas",
    state: "TX",
    email: "bbq@barn.com",
    phone_number: "(214) 888-7777",
  },
  {
    restaurant_id: 20,
    name: "Tapas & Tings",
    description: "Small plates and bold Caribbean flavors.",
    city: "Atlanta",
    state: "GA",
    email: "contact@tapasandtings.com",
    phone_number: "(404) 321-9090",
  },
];

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


  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete this listing?")) {
      // Shows a confirmation popup dialog to the user
      fetch(`/api/manager/restaurants/${id}`, { method: "DELETE" }).then(() => {
        setRestaurants((prev) => prev.filter((r) => r.id !== id));
      });
    }
  };

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
