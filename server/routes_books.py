# routes_books.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import asc, desc
from models import db, Book, BookAudit
from schemas import BookSchema, BookAuditSchema
from routes_users import current_user, is_admin
import json

books_bp = Blueprint("books", __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)
audit_schema = BookAuditSchema()

@books_bp.route("/filter", methods=["GET"])
def filter_books():
    """
    Public endpoint: filter/search/sort/paginate books
    Example: GET /api/filter?publisher=xx&level=pp1&subject=math&sort=title&direction=asc
    """
    from math import ceil

    publisher_query = request.args.get("publisher", "").strip()
    level_query = request.args.get("level", "").strip()
    subject_query = request.args.get("subject", "").strip()
    sort_by = request.args.get("sort", "title")
    direction = request.args.get("direction", "asc")

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    q = Book.query

    # Filter
    if publisher_query:
        q = q.filter(Book.publisher.ilike(f"%{publisher_query}%"))
    if level_query:
        q = q.filter(Book.level.ilike(f"%{level_query}%"))
    if subject_query:
        q = q.filter(Book.title.ilike(f"%{subject_query}%"))

    # Sort
    if sort_by == "price":
        col = Book.price
    else:
        col = Book.title

    if direction == "desc":
        q = q.order_by(desc(col))
    else:
        q = q.order_by(asc(col))

    total_count = q.count()
    pages = ceil(total_count / limit)
    offset_val = (page - 1) * limit

    books_list = q.offset(offset_val).limit(limit).all()
    data = books_schema.dump(books_list)

    return jsonify({
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "total_pages": pages,
        "data": data
    }), 200


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Public endpoint: get single book by ID."""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": f"No book found with ID {book_id}"}), 404

    return jsonify(book_schema.dump(book)), 200


@books_bp.route("/books", methods=["POST"])
@jwt_required()
def create_book():
    """
    Create a new book. Only admin can create.
    Body: { "title": "...", "publisher": "...", etc. }
    """
    user = current_user()
    if not user or not is_admin(user):
        return jsonify({"error": "Admin permission required"}), 403

    data = request.get_json() or {}
    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()

    # Log the CREATE action
    audit = BookAudit(
        user_id=user.id,
        book_id=new_book.id,
        action="CREATE",
        old_data=None,
        new_data=json.dumps(book_schema.dump(new_book)),
    )
    db.session.add(audit)
    db.session.commit()

    return jsonify(book_schema.dump(new_book)), 201


@books_bp.route("/books/<int:book_id>", methods=["PUT"])
@jwt_required()
def update_book(book_id):
    """
    Update an existing book. Only admin can update.
    """
    user = current_user()
    if not user or not is_admin(user):
        return jsonify({"error": "Admin permission required"}), 403

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json() or {}
    errors = book_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    # Keep old data for logging
    old_data = book_schema.dump(book)

    for key, val in data.items():
        setattr(book, key, val)

    db.session.commit()

    # Keep new data for logging
    new_data = book_schema.dump(book)
    audit = BookAudit(
        user_id=user.id,
        book_id=book.id,
        action="UPDATE",
        old_data=json.dumps(old_data),
        new_data=json.dumps(new_data),
    )
    db.session.add(audit)
    db.session.commit()

    return jsonify(book_schema.dump(book)), 200


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    """
    Delete a book. Only admin can delete.
    """
    user = current_user()
    if not user or not is_admin(user):
        return jsonify({"error": "Admin permission required"}), 403

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    old_data = book_schema.dump(book)

    db.session.delete(book)
    db.session.commit()

    # Log the DELETE action
    audit = BookAudit(
        user_id=user.id,
        book_id=book_id,
        action="DELETE",
        old_data=json.dumps(old_data),
        new_data=None,
    )
    db.session.add(audit)
    db.session.commit()

    return jsonify({"message": f"Book {book_id} deleted"}), 200
