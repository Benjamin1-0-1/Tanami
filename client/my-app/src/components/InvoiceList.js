// InvoicesList.jsx
import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../auth/AuthContext";

function InvoicesList() {
  const { token } = useContext(AuthContext);
  const [invoices, setInvoices] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;
    const fetchInvoices = async () => {
      try {
        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };
        const res = await axios.get("http://127.0.0.1:5000/api/invoices", config);
        setInvoices(res.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load invoices");
      }
    };
    fetchInvoices();
  }, [token]);

  return (
    <div style={{ margin: "2rem" }}>
      <h2>My Past Invoices</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {invoices.map((inv) => (
          <li key={inv.id}>
            Invoice #{inv.id} | Date: {inv.created_at} | Total: {inv.total_price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default InvoicesList;
