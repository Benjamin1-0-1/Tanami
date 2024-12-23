import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { AuthProvider } from "./auth/AuthProvider";
import { AuthContext } from "./auth/AuthContext";

import Login from "./components/Login";
import Register from "./components/Register";
import BookList from "./components/BookList";
import BookForm from "./components/BookForm";
import InvoicePage from "./components/InvoicePage";
import InvoicesList from "./components/InvoiceList";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />
        <div style={{ padding: "1rem" }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Book pages */}
            <Route path="/books" element={<BookList />} />
            <Route path="/books/create" element={<BookForm />} />
            <Route path="/books/edit/:id" element={<BookForm />} />

            {/* Invoice pages */}
            <Route path="/invoices" element={<InvoicePage />} />
            <Route path="/invoices/past" element={<InvoicesList />} />

            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}

function Navbar() {
  // Show link to "Logout" or "Login" based on token
  const { token, setToken } = React.useContext(AuthContext);

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <nav style={{ display: "flex", gap: "1rem", background: "#ddd", padding: "1rem" }}>
      <Link to="/">Home</Link>
      <Link to="/books">Books</Link>
      {token ? (
        <>
          <Link to="/books/create">Add Book</Link>
          <Link to="/invoices">Create/View Invoice</Link>
          <Link to="/invoices/past">Past Invoices</Link>

          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/register">Register</Link>
          <Link to="/login">Login</Link>
        </>
      )}
    </nav>
  );
}

function Home() {
  return <h2>Welcome to the Bookstore</h2>;
}

function NotFound() {
  return <h2>404 - Not Found</h2>;
}

export default App;
