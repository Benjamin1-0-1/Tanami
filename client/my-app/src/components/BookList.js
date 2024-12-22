import React, { useState, useEffect, useContext } from "react";
import api from "../services/api";
import { AuthContext } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";

const BookList = () => {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();

  // Filters
  const [publisherQuery, setPublisherQuery] = useState("");
  const [levelQuery, setLevelQuery] = useState("");
  const [subjectQuery, setSubjectQuery] = useState("");

  // Sort
  const [sortBy, setSortBy] = useState("title");
  const [direction, setDirection] = useState("asc");

  // Pagination
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(5);

  // Data
  const [books, setBooks] = useState([]);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [errMsg, setErrMsg] = useState("");

  // 1) This function calls /api/filter with the current queries
  const fetchFilteredBooks = async () => {
    setLoading(true);
    setErrMsg("");
    try {
      const res = await api.get("/api/filter", {
        params: {
          publisher: publisherQuery || undefined,
          level: levelQuery || undefined,
          subject: subjectQuery || undefined,
          sort: sortBy,
          direction: direction,
          page: page,
          limit: limit,
        },
      });
      const data = res.data;
      setBooks(data.data);
      setTotalPages(data.total_pages);
    } catch (error) {
      console.error(error);
      setErrMsg("Error fetching books");
    } finally {
      setLoading(false);
    }
  };

  // 2) If you want a "get all books" approach using /api/books (no filters):
  //    You can do this if you prefer a separate endpoint for “all books”.
  const fetchAllBooks = async () => {
    setLoading(true);
    setErrMsg("");
    try {
      const res = await api.get("/api/books");
      setBooks(res.data);
      setTotalPages(1);  // since /api/books returns all
    } catch (error) {
      console.error(error);
      setErrMsg("Error fetching all books");
    } finally {
      setLoading(false);
    }
  };

  // 3) We'll primarily use fetchFilteredBooks whenever the queries change
  useEffect(() => {
    fetchFilteredBooks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [publisherQuery, levelQuery, subjectQuery, sortBy, direction, page, limit]);

  // 4) Deleting a book
  const handleDelete = async (id) => {
    if (!token) {
      alert("You must be logged in to delete a book.");
      return;
    }
    if (window.confirm("Are you sure you want to delete this book?")) {
      try {
        await api.delete(`/api/books/${id}`);
        // after deletion, refresh the list
        fetchFilteredBooks();
      } catch (error) {
        console.error("Delete error:", error);
      }
    }
  };

  // 5) A "View All" button that resets queries
  const handleViewAll = () => {
    // Clear all filters so fetchFilteredBooks returns everything
    setPublisherQuery("");
    setLevelQuery("");
    setSubjectQuery("");
    setPage(1);
    setLimit(10); // optional, show more items
    // Or if you prefer calling /api/books:
    // fetchAllBooks();
  };

  return (
    <div style={{ maxWidth: "800px", margin: "2rem auto" }}>
      <h2>Book List (Filter & Sort)</h2>
      <div>
        <label>Publisher: </label>
        <input
          value={publisherQuery}
          onChange={(e) => {
            setPage(1);
            setPublisherQuery(e.target.value);
          }}
        />

        <label> Level: </label>
        <input
          value={levelQuery}
          onChange={(e) => {
            setPage(1);
            setLevelQuery(e.target.value);
          }}
        />

        <label> Subject: </label>
        <input
          value={subjectQuery}
          onChange={(e) => {
            setPage(1);
            setSubjectQuery(e.target.value);
          }}
        />
      </div>

      <div style={{ marginTop: "1rem" }}>
        <label>Sort By: </label>
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="title">Title</option>
          <option value="price">Price</option>
        </select>

        <label> Direction: </label>
        <select value={direction} onChange={(e) => setDirection(e.target.value)}>
          <option value="asc">Asc</option>
          <option value="desc">Desc</option>
        </select>

        <label> Page: </label>
        <input
          style={{ width: "60px" }}
          type="number"
          value={page}
          onChange={(e) => setPage(Number(e.target.value))}
        />

        <label> Limit: </label>
        <input
          style={{ width: "60px" }}
          type="number"
          value={limit}
          onChange={(e) => {
            setPage(1);
            setLimit(Number(e.target.value));
          }}
        />

        {/* New button to reset or get all */}
        <button onClick={handleViewAll} style={{ marginLeft: "1rem" }}>
          View All
        </button>
      </div>

      {loading ? <p>Loading...</p> : null}
      {errMsg && <p style={{ color: "red" }}>{errMsg}</p>}

      <table border="1" cellPadding="4" style={{ marginTop: "1rem", width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Publisher</th>
            <th>Level</th>
            <th>Title</th>
            <th>Price</th>
            <th>Status</th>
            {token && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {books.map((bk) => (
            <tr key={bk.id}>
              <td>{bk.id}</td>
              <td>{bk.publisher}</td>
              <td>{bk.level}</td>
              <td>{bk.title}</td>
              <td>{bk.price}</td>
              <td>{bk.status}</td>
              {token && (
                <td>
                  <button onClick={() => navigate(`/books/edit/${bk.id}`)}>
                    Edit
                  </button>
                  <button onClick={() => handleDelete(bk.id)}>Delete</button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: "1rem" }}>
        <p>
          Page {page} of {totalPages}
        </p>
        <button
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page <= 1}
        >
          Prev
        </button>
        <button
          onClick={() => setPage((p) => (p < totalPages ? p + 1 : p))}
          disabled={page >= totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default BookList;
