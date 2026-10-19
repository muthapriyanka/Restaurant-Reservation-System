const LOCAL_API_BASE_URL = "http://localhost:8000/api";
const RENDER_API_BASE_URL =
  "https://restaurant-reservation-api-6djs.onrender.com/api";

export const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL ||
  (process.env.NODE_ENV === "production"
    ? RENDER_API_BASE_URL
    : LOCAL_API_BASE_URL);
