import React, { useState } from "react";
import axios from "axios";

function QuoteGenerator({ customerList, setCustomerList }) {
  const [newTitle, setNewTitle] = useState("");
  const [quote, setQuote] = useState(null);
  const [error, setError] = useState("");

  // Add a book title to the customer's list
  const handleAddTitle = () => {
    if (newTitle.trim()) {
      setCustomerList([...customerList, newTitle.trim()]);
      setNewTitle("");
    }
  };

  // Generate a quote by sending the list of titles to the backend
  const handleGenerateQuote = async () => {
    try {
      setError("");
      setQuote(null);

      const response = await axios.post("http://127.0.0.1:5000/api/generate-quote", {
        titles: customerList,
      });

      setQuote(response.data);
    } catch (err) {
      console.error(err);
      setError("Error generating quote. Check the console or server logs.");
    }
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "1rem" }}>
      <h3>Customer Book List</h3>
      <input
        type="text"
        placeholder="Enter book title EXACTLY..."
        value={newTitle}
        onChange={(e) => setNewTitle(e.target.value)}
      />
      <button onClick={handleAddTitle}>Add</button>

      <ul>
        {customerList.map((title, idx) => (
          <li key={idx}>{title}</li>
        ))}
      </ul>

      <button onClick={handleGenerateQuote}>Get Quote</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {quote && (
        <div style={{ marginTop: "1rem", background: "#f9f9f9", padding: "1rem" }}>
          <h4>Quote Result:</h4>
          <p><strong>Requested Titles:</strong> {quote.requested_titles.join(", ")}</p>
          <p><strong>Total Price:</strong> {quote.total_price}</p>
          <h5>Matched Books:</h5>
          <ul>
            {quote.matched_books.map((mb, i) => (
              <li key={i}>
                {mb.title} (Level: {mb.level}, Price: {mb.price})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default QuoteGenerator;
