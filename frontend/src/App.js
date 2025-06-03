import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import Login from "./Login";
import WelcomePage from "./WelcomePage";
//import CustomerView from './CustomerView';
import AddRestaurantForm from "./AddRestaurantForm";
import AdminAnalytics from "./AdminAnalytics";
import AdminDashboard from "./AdminDashboard";
import BookRestaurant from "./BookRestaurant";
import CustomerBookings from "./CustomerBookings";
import CustomerRestaurantSearch from "./CustomerRestaurantSearch";
import ManagerDashboard from "./ManagerDashboard";
import ProtectedRoute from "./ProtectedRoute";
import ReadReview from "./ReadReview";
import Register from "./Register"; // Import the Register component
import RestaurantDetails from "./RestaurantDetails";
import RestaurantList from "./RestaurantList";

import "./styles.css";
import UpdateRestaurant from "./UpdateRestaurant";

// Check if the user is authenticated and get their role from localStorage
const isAuthenticated = () => {
  return localStorage.getItem("role") !== null;
};

// Function to get the current user role
const getRole = () => {
  return localStorage.getItem("role");
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Login Page (Home page) */}
        <Route path="/" element={<WelcomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        <Route
          path="/managerDashboard"
          element={
            <ProtectedRoute>
              <ManagerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/adminDashboard"
          element={
            <ProtectedRoute>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/list"
          element={
            <ProtectedRoute>
              <RestaurantList />
            </ProtectedRoute>
          }
        />
        <Route
          path="/book/:id"
          element={
            <ProtectedRoute>
              <BookRestaurant />
            </ProtectedRoute>
          }
        />
        <Route
          path="/update/:id"
          element={
            <ProtectedRoute>
              <UpdateRestaurant />
            </ProtectedRoute>
          }
        />
        <Route
          path="/adminAnalytics"
          element={
            <ProtectedRoute>
              <AdminAnalytics />
            </ProtectedRoute>
          }
        />
        <Route
          path="/addRestaurantForm"
          element={
            <ProtectedRoute>
              <AddRestaurantForm />
            </ProtectedRoute>
          }
        />
        <Route
          path="/custDashboard"
          element={
            <ProtectedRoute>
              <CustomerRestaurantSearch />
            </ProtectedRoute>
          }
        />
        <Route
          path="/my-bookings"
          element={
            <ProtectedRoute>
              <CustomerBookings />
            </ProtectedRoute>
          }
        />
        <Route
          path="/read-review"
          element={
            <ProtectedRoute>
              <ReadReview />
            </ProtectedRoute>
          }
        />
        <Route
          path="/restaurant-details"
          element={
            <ProtectedRoute>
              <RestaurantDetails />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
