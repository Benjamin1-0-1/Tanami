import api from "./api";

export const registerUser = async (username, password) => {
  const response = await api.post("/api/register", { username, password });
  return response.data;
};

export const loginUser = async (username, password) => {
  const response = await api.post("/api/login", { username, password });
  return response.data; // should contain { access_token: "..." }
};
