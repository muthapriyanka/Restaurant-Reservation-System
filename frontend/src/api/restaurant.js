import axios from 'axios';

// Get restaurants by manager
export const getRestaurantsByManager = async () => {
  const response = await axios.get('/manager/restaurants');
  return response.data;
};

// Create a restaurant
export const createRestaurant = async (restaurantData) => {
  const response = await axios.post('/manager/restaurants', restaurantData);
  return response.data;
};

// Get all restaurants (admin view)
export const getAllRestaurants = async () => {
  const response = await axios.get('/admin/restaurants');
  return response.data;
};
