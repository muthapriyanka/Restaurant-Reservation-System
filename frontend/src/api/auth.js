import API from "../api";

export const loginUser = async (formData) => {
  try {
    const response = await API.post("/login", formData);
    return response.data;
  } catch (error) {
    console.error("Login failed:", error);
    throw error;
  }
};

export const registerUser = async (data) => {
  try {
    const response = await API.post("/register", data);
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const getAllAdminRestaurants = async (data) => {
  try {
    const response = await API.get("/admin/restaurants");
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const adminApproveRestaurant = async (data) => {
  try {
    const response = await API.put(
      `/admin/restaurants/${data.restaurantId}/approve`
    );
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const adminRemoveRestaurant = async (data) => {
  try {
    const response = await API.delete(
      `/admin/restaurants/${data.restaurantId}`
    );
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const managerAddRestaurant = async (data) => {
  try {
    const response = await API.post("/manager/restaurants", data);
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const managerAddOperatingHours = async (restaurantId, data) => {
  try {
    // Transform the data to match the expected format
    const formattedData = {
      operating_hours: data.map((hour) => ({
        day_of_week: hour.day_of_week.toLowerCase(),
        opening_time:
          hour.opening_time.length === 5
            ? `${hour.opening_time}:00`
            : hour.opening_time,
        closing_time:
          hour.closing_time.length === 5
            ? `${hour.closing_time}:00`
            : hour.closing_time,
      })),
    };
    const response = await API.post(
      `/manager/restaurants/${restaurantId}/hours`,
      formattedData
    );
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const getAllRestaurantsForManager = async (data) => {
  try {
    const response = await API.get("/manager/restaurants");
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const getRestaurantDetailForManager = async (data) => {
  try {
    const response = await API.get(`/restaurants/${data.id}`);
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const updateRestaurantForManager = async (data) => {
  try {
    const response = await API.put(
      `/manager/restaurants/${data.id}`,
      data.restaurant
    );
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw error;
  }
};

export const managerUpdateOperatingHours = async (restaurantId, data) => {
  try {
    // Transform the data to match the expected format
    const formattedData = {
      operating_hours: data.map((hour) => ({
        day_of_week: hour.day_of_week.toLowerCase(),
        opening_time:
          hour.opening_time.length === 5
            ? `${hour.opening_time}:00`
            : hour.opening_time,
        closing_time:
          hour.closing_time.length === 5
            ? `${hour.closing_time}:00`
            : hour.closing_time,
      })),
    };

    const response = await API.put(
      `/manager/restaurants/${restaurantId}/hours`,
      formattedData
    );
    return response.data;
  } catch (error) {
    console.error("Operating hours update failed:", error);
    throw error;
  }
};

export const getAllBookings = async () => {
  try {
    const response = await API.get("/reservations");
    return response.data;
  } catch (error) {
    console.error("Booking retrieval for customer failed:", error);
    throw error;
  }
};

export const addReview = async (data) => {
  try {
    const response = await API.post(
      `restaurants/${data.restaurant_id}/reviews`,
      data
    );
    return response.data;
  } catch (error) {
    alert(error.response.data.detail);
    console.error("review failed:", error);
    throw error;
  }
};

export const getAllRestaurantsForCustomers = async () => {
  try {
    const response = await API.get("/customer/restaurants");
    return response.data;
  } catch (error) {
    console.error("Booking retrieval for customer failed:", error);
    throw error;
  }
};

export const getAllReviewsForRestaurant = async (data) => {
  try {
    const response = await API.get(`/restaurants/${data.restaurantId}/reviews`);
    return response.data;
  } catch (error) {
    console.error("Review get restarurant failed:", error);
    throw error;
  }
};

export const bookReservation = async (data) => {
  try {
    const response = await API.post("/reservations", data);
    return response.data;
  } catch (error) {
    alert(error.response.data.detail);
    console.error("review failed:", error);
    throw error;
  }
};

export const managerAddTables = async (restaurantId, data) => {
  try {
    const response = await API.post(
      `/manager/restaurants/${restaurantId}/tables`,
      data
    );
    return response.data;
  } catch (error) {
    console.error("Tables add failed:", error);
    throw error;
  }
};

export const managerUpdateTables = async (restaurantId, data) => {
  try {
    const response = await API.put(
      `/manager/restaurants/${restaurantId}/tables`,
      data
    );
    return response.data;
  } catch (error) {
    console.error("Tables update failed:", error);
    throw error;
  }
};

export const cancelCustomerBooking = async (data) => {
  try {
    const response = await API.delete(`/reservations/${data.reservation_id}`);
    return response.data;
  } catch (error) {
    console.error("Removing booking failed for customer:", error);
    throw error;
  }
};
