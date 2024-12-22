// BookSelector.jsx
import React, { useState, useEffect } from "react";

function BookSelector({ books, onSelectionChange }) {
  const [selectedIds, setSelectedIds] = useState([]);

  const handleToggle = (bookId) => {
    if (selectedIds.includes(bookId)) {
      setSelectedIds(selectedIds.filter((id) => id !== bookId));
    } else {
      setSelectedIds([...selectedIds, bookId]);
    }
  };

  useEffect(() => {
    onSelectionChange(selectedIds);
  }, [selectedIds, onSelectionChange]);

  return (
    <div style={{ margin: "1rem 0" }}>
      <h3>Select Books:</h3>
      {books.map((b) => (
        <div key={b.id}>
          <label>
            <input
              type="checkbox"
              checked={selectedIds.includes(b.id)}
              onChange={() => handleToggle(b.id)}
            />
            {b.title} (Price: {b.price})
          </label>
        </div>
      ))}
    </div>
  );
}

export default BookSelector;
