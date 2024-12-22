import React, { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import { AuthContext } from "../auth/AuthContext";

const BookForm = () => {
  const { token } = useContext(AuthContext);
  const { id } = useParams(); // if we have an ID, it's an edit
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    publisher: "",
    level: "",
    isbn: "",
    title: "",
    price: "",
    status: "",
  });
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    if (!token) {
      alert("You must be logged in to access this page.");
      navigate("/login");
    } else {
      if (id) {
        // editing existing book
        fetchBook(id);
      }
    }
    // eslint-disable-next-line
  }, [id, token]);

  const fetchBook = async (bookId) => {
    try {
      const res = await api.get(`/api/books/${bookId}`);
      setFormData({
        publisher: res.data.publisher || "",
        level: res.data.level || "",
        isbn: res.data.isbn || "",
        title: res.data.title || "",
        price: res.data.price ?? "",
        status: res.data.status || "",
      });
    } catch (error) {
      console.error(error);
      setErrorMsg("Error loading book data");
    }
  };

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg("");
    try {
      if (id) {
        // Update existing
        await api.put(`/api/books/${id}`, {
          ...formData,
          price: parseFloat(formData.price) || 0,
        });
        alert("Book updated");
      } else {
        // Create new
        await api.post("/api/books", {
          ...formData,
          price: parseFloat(formData.price) || 0,
        });
        alert("New book created");
      }
      navigate("/books");
    } catch (error) {
      console.error(error);
      setErrorMsg(error.response?.data?.error || "Save failed");
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <h2>{id ? "Edit Book" : "Create Book"}</h2>
      {errorMsg && <p style={{ color: "red" }}>{errorMsg}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Publisher:</label>
          <input
            name="publisher"
            value={formData.publisher}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Level:</label>
          <input
            name="level"
            value={formData.level}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>ISBN:</label>
          <input
            name="isbn"
            value={formData.isbn}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Title: (required)</label>
          <input
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label>Price:</label>
          <input
            name="price"
            type="number"
            value={formData.price}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Status:</label>
          <input
            name="status"
            value={formData.status}
            onChange={handleChange}
          />
        </div>

        <button type="submit">{id ? "Update" : "Create"}</button>
      </form>
    </div>
  );
};

export default BookForm;
