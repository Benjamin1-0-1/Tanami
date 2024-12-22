import React, { useState, useContext } from "react";
import { AuthContext } from "../auth/AuthContext";
import { loginUser } from "../services/authService";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const { setToken } = useContext(AuthContext);
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser(username, password);
      if (data.access_token) {
        setToken(data.access_token);
        navigate("/books"); // go to books list
      } else {
        setErrorMsg("Something went wrong.");
      }
    } catch (error) {
      setErrorMsg(error.response?.data?.error || "Login failed");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "2rem auto" }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label><br />
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label><br />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {errorMsg && <p style={{ color: "red" }}>{errorMsg}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
