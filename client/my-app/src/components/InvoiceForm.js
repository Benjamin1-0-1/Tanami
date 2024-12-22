// InvoiceForm.jsx
import React, { useContext, useState } from "react";
import axios from "axios";
import { AuthContext } from "../auth/AuthContext";

function InvoiceForm({ selectedBookIds }) {
  const { token } = useContext(AuthContext);
  const [invoice, setInvoice] = useState(null);
  const [error, setError] = useState("");

  const handleCreateInvoice = async () => {
    if (!token) {
      setError("You must be logged in to create an invoice");
      return;
    }
    if (selectedBookIds.length === 0) {
      setError("No books selected");
      return;
    }
    setError("");
    setInvoice(null);

    try {
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      };
      const body = {
        book_ids: selectedBookIds
        // or you can pass quantities: [1, 2, 1] if needed
      };
      const res = await axios.post("http://127.0.0.1:5000/api/invoices", body, config);
      setInvoice(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to create invoice");
    }
  };

  return (
    <div>
      <button onClick={handleCreateInvoice}>Create Invoice</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {invoice && (
        <div style={{ marginTop: "1rem", border: "1px solid #ccc", padding: "1rem" }}>
          <h4>Invoice #{invoice.id}</h4>
          <p>User: {invoice.user_name}</p>
          <p>Created At: {invoice.created_at}</p>
          <p>Total: {invoice.total_price}</p>
          <ul>
            {invoice.items.map((it, idx) => (
              <li key={idx}>
                Book: {it.title}, Price: {it.book_price}, Qty: {it.quantity}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default InvoiceForm;
