import React, { useState } from "react";
import { AuthContext } from "./AuthContext";

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => {
    // On refresh, read token from localStorage if available
    return localStorage.getItem("jwtToken") || null;
  });

  const handleSetToken = (newToken) => {
    setToken(newToken);
    if (newToken) {
      localStorage.setItem("jwtToken", newToken);
    } else {
      localStorage.removeItem("jwtToken");
    }
  };

  return (
    <AuthContext.Provider value={{ token, setToken: handleSetToken }}>
      {children}
    </AuthContext.Provider>
  );
};
