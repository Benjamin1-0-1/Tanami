# seed.py

import json
from app import create_app  # Import your factory
from models import db, Book

def seed_database():
    """
    Loads data from books_data.json & inserts into DB.
    """
    app = create_app()
    with app.app_context():
        # 1) Create tables if not exist
        db.create_all()

        # 2) Clear old data (optional in production!)
        Book.query.delete()

        # 3) Load from JSON
        print("Loading data from books_data.json...")
        with open("books.json", "r", encoding="utf-8") as f:
            seed_data = json.load(f)

        # 4) Insert records
        print("Inserting records...")
        for block in seed_data:
            publisher_name = block["publisher"]
            level_str = block["level"]
            for item in block["items"]:
                new_book = Book(
                    publisher=publisher_name,
                    level=level_str,
                    isbn=item.get("isbn"),
                    title=item["title"],
                    price=item.get("price"),
                    status=item.get("status")
                )
                db.session.add(new_book)

        # 5) Commit
        db.session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    seed_database()
