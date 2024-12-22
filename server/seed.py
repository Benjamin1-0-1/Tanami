# seed.py
from app import db, app
from models import Book

# --------------------------------------------------------------
# 1) DEFINE / LOAD YOUR MASSIVE BOOK DATA
#    For clarity, here’s a highly abbreviated snippet of your data.
#    You can store the entire dataset in a JSON file and read it in,
#    or just define it as a Python variable.
# --------------------------------------------------------------
seed_data = [
    {
        "publisher": "KENYA LITERATURE BUREAU",
        "level": "pp1",
        "items": [
            {
                "isbn": None,
                "title": "KLB skillgrow language activities",
                "price": 447.00,
                "status": "APPROVED"
            },
            {
                "isbn": None,
                "title": "KLB skillgrow mazoezi ya lugha",
                "price": 401.00,
                "status": "APPROVED"
            },
            # ... more items ...
        ]
    },
    {
        "publisher": "LONGHORN",
        "level": "pp1",
        "items": [
            {
                "isbn": None,
                "title": "longhorn language activities",
                "price": 650,
                "status": "APPROVED"
            },
            {
                "isbn": None,
                "title": "longhornmathematics activities",
                "price": 620,
                "status": "APPROVED"
            }
        ]
    },
    # ADD THE REST OF YOUR BIG LIST HERE ...
]


# --------------------------------------------------------------
# 2) CREATE ALL TABLES (if not exist) AND INSERT (SEED) THE DATA
# --------------------------------------------------------------
def seed_database():
    with app.app_context():
        # Create the tables if they don’t already exist
        print("Creating tables...")
        db.create_all()

        # Clear existing data (optional; be careful in production!)
        print("Clearing old data...")
        Book.query.delete()

        # Insert new records
        print("Seeding new data...")
        for block in seed_data:
            publisher_name = block["publisher"]
            level = block["level"]
            for item in block["items"]:
                new_book = Book(
                    publisher=publisher_name,
                    level=level,
                    isbn=item.get("isbn"),
                    title=item["title"],
                    price=item.get("price"),
                    status=item.get("status")
                )
                db.session.add(new_book)

        # Commit all changes
        db.session.commit()
        print("Seeding complete!")


if __name__ == "__main__":
    seed_database()
