# commands.py
import json
from flask import current_app
from flask.cli import AppGroup
from models import Book, db
from math import isnan

cli = AppGroup("custom")

@cli.command("seed-data")
def seed_data():
    """
    Example command to seed the DB from 'books.json'.
    Usage:
        flask custom seed-data
    """
    print("Seeding data from books.json ...")
    try:
        with open("books.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("books.json not found!")
        return

    # Clear old data
    Book.query.delete()

    # data is expected to be an array of objects in the new structure:
    # [
    #   {
    #       "publisher": "KENYA LITERATURE BUREAU",
    #       "PP1": [
    #         { "title": "KLB skillgrow language activities", "price": 447.0, "status": "APPROVED" },
    #         ...
    #       ],
    #       "PP2": [ ... ],
    #       ...
    #   },
    #   {
    #       "publisher": "LONGHORN",
    #       "PP1": [ ... ],
    #       ...
    #   }
    # ]

    for publisher_obj in data:
        publisher_name = publisher_obj.get("publisher", "UNKNOWN")
        for key, val in publisher_obj.items():
            if key == "publisher":
                continue
            level_name = key  # e.g. "PP1", "GRADE1", etc.
            if isinstance(val, list):
                for item in val:
                    new_book = Book(
                        publisher=publisher_name,
                        level=level_name,
                        isbn=item.get("isbn"),
                        title=item["title"],
                        price=item.get("price"),
                        status=item.get("status")
                    )
                    db.session.add(new_book)
    db.session.commit()
    print("Seeding complete!")


def init_app(app):
    """
    Attach the custom CLI group to the app.
    """
    app.cli.add_command(cli)
