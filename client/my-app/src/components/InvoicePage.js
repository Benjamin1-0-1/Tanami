// InvoicePage.jsx

import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../auth/AuthContext"; // to get JWT token

function InvoicePage() {
  const { token } = useContext(AuthContext);

  // For searching books
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchError, setSearchError] = useState("");

  // For building the invoice
  const [selectedBooks, setSelectedBooks] = useState([]);
    // array of objects: {id, title, price}
    // or you can store just IDs

  const [invoice, setInvoice] = useState(null);
  const [invoiceError, setInvoiceError] = useState("");

  // For viewing past invoices (optional)
  const [showPastInvoices, setShowPastInvoices] = useState(false);
  const [pastInvoices, setPastInvoices] = useState([]);
  const [pastError, setPastError] = useState("");

  // 1) Searching for books
  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setSearchError("Type something to search");
      return;
    }
    setSearchError("");
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/filter", {
        params: {
          subject: searchQuery,   // or 'publisher', or combine them
          // publisher: publisherQuery,
          // level: levelQuery,
          // subject: subjectQuery,
          limit: 50,
        },
      });
      if (res.data.data) {
        // /api/filter returns { data: [...] }
        setSearchResults(res.data.data);
      } else {
        // or if /api/filter just returns an array
        setSearchResults(res.data);
      }
    } catch (err) {
      console.error(err);
      setSearchError("Failed to search books");
    }
  };

  // 2) "Add" a book to the invoice
  const handleAddBook = (bk) => {
    // check if it's already in selectedBooks
    if (selectedBooks.find((x) => x.id === bk.id)) {
      return; // already added
    }
    // add
    setSelectedBooks([...selectedBooks, { id: bk.id, title: bk.title, price: bk.price }]);
  };

  // 3) Remove from invoice
  const handleRemoveBook = (id) => {
    setSelectedBooks(selectedBooks.filter((bk) => bk.id !== id));
  };

  // 4) Create the invoice
  const handleCreateInvoice = async () => {
    if (!token) {
      setInvoiceError("You must be logged in");
      return;
    }
    if (selectedBooks.length === 0) {
      setInvoiceError("No books selected for invoice");
      return;
    }

    // gather just the IDs
    const bookIds = selectedBooks.map((bk) => bk.id);

    try {
      setInvoiceError("");
      setInvoice(null);

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      };
      const body = { book_ids: bookIds };
      const res = await axios.post("http://127.0.0.1:5000/api/invoices", body, config);
      setInvoice(res.data);
      // clear the selectedBooks if you want
      setSelectedBooks([]);
    } catch (err) {
      console.error(err);
      setInvoiceError("Failed to create invoice");
    }
  };

  // 5) Toggle or fetch past invoices
  const handleTogglePastInvoices = async () => {
    setShowPastInvoices(!showPastInvoices);
    if (!showPastInvoices) {
      // we are about to show them, so fetch
      try {
        setPastError("");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const res = await axios.get("http://127.0.0.1:5000/api/invoices", config);
        setPastInvoices(res.data);
      } catch (err) {
        console.error(err);
        setPastError("Failed to load past invoices");
      }
    }
  };

  return (
    <div style={{ margin: "2rem" }}>
      <h2>Invoice Page (Search + Add to Invoice)</h2>

      {/* SEARCH SECTION */}
      <div style={{ border: "1px solid #ccc", padding: "1rem" }}>
        <h3>Search Books</h3>
        <input
          type="text"
          placeholder="Search by title or subject..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
        {searchError && <p style={{ color: "red" }}>{searchError}</p>}

        {/* RESULTS */}
        {searchResults.length > 0 && (
          <div style={{ marginTop: "1rem" }}>
            <h4>Results:</h4>
            {searchResults.map((bk) => (
              <div key={bk.id} style={{ marginBottom: "0.5rem" }}>
                Title: {bk.title} | Price: {bk.price}{" "}
                <button onClick={() => handleAddBook(bk)}>Add to Invoice</button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* SELECTED BOOKS for INVOICE */}
      <div style={{ border: "1px solid #ccc", padding: "1rem", marginTop: "1rem" }}>
        <h3>Invoice Items</h3>
        {selectedBooks.length === 0 && <p>No books added yet</p>}
        {selectedBooks.length > 0 && (
          <ul>
            {selectedBooks.map((bk) => (
              <li key={bk.id}>
                {bk.title} (Price: {bk.price})
                <button onClick={() => handleRemoveBook(bk.id)} style={{ marginLeft: "1rem" }}>
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
        {/* CREATE INVOICE */}
        <button onClick={handleCreateInvoice}>Create Invoice</button>
        {invoiceError && <p style={{ color: "red" }}>{invoiceError}</p>}
        {invoice && (
          <div style={{ marginTop: "1rem", border: "1px solid green", padding: "1rem" }}>
            <h4>Invoice #{invoice.id} Created!</h4>
            <p>User: {invoice.user_name}</p>
            <p>Created At: {invoice.created_at}</p>
            <p>Total: {invoice.total_price}</p>
            <ul>
              {invoice.items.map((it, idx) => (
                <li key={idx}>
                  Book ID: {it.book_id}, Title: {it.title}, Price: {it.book_price}, Qty: {it.quantity}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* PAST INVOICES */}
      <div style={{ marginTop: "2rem" }}>
        <button onClick={handleTogglePastInvoices}>
          {showPastInvoices ? "Hide" : "View"} Past Invoices
        </button>
        {showPastInvoices && (
          <div style={{ marginTop: "1rem" }}>
            {pastError && <p style={{ color: "red" }}>{pastError}</p>}
            {pastInvoices.length === 0 && <p>No past invoices found</p>}
            <ul>
              {pastInvoices.map((inv) => (
                <li key={inv.id}>
                  Invoice #{inv.id} - Date: {inv.created_at}, Total: {inv.total_price}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default InvoicePage;
