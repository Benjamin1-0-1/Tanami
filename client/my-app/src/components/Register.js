import React, { useState } from "react";
import { registerUser } from "../services/authService";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await registerUser(username, password);
      if (data.message) {
        setMsg("Registration successful. You can now login.");
        setUsername("");
        setPassword("");
        setTimeout(() => {
          navigate("/login");
        }, 1500);
      }
    } catch (error) {
      setMsg(error.response?.data?.error || "Registration failed");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "2rem auto" }}>
      <h2>Register</h2>
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
        {msg && <p>{msg}</p>}
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
