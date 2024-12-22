import axios from "axios";

// Base URL of your Flask backend
const BASE_URL = "http://127.0.0.1:5000";

const api = axios.create({
  baseURL: BASE_URL,
});

// Optionally, we can intercept requests and attach the token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("jwtToken");
  if (token && config.url !== "/api/login" && config.url !== "/api/register") {
    // Attach token if it's not the login/register endpoint
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
