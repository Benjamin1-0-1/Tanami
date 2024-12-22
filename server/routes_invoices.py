# routes_invoices.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, Book, Invoice, InvoiceItem
from routes_users import current_user  # A helper function to get the logged-in user

invoices_bp = Blueprint("invoices", __name__)

@invoices_bp.route("/invoices", methods=["POST"])
@jwt_required()
def create_invoice():
    """
    Creates an invoice for the current user.
    Expects JSON:
    {
      "book_ids": [1, 2, 3],
      "quantities": [1, 2, 1]  # optional if you want quantity
    }

    Returns the created invoice with line items.
    """
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json() or {}
    book_ids = data.get("book_ids")
    if not book_ids:
        return jsonify({"error": "Missing 'book_ids' array"}), 400

    quantities = data.get("quantities", [1]*len(book_ids))
    if len(book_ids) != len(quantities):
        return jsonify({"error": "Mismatch: book_ids & quantities lengths"}), 400

    # Fetch the books
    books = Book.query.filter(Book.id.in_(book_ids)).all()
    if len(books) != len(book_ids):
        return jsonify({"error": "Some book IDs not found"}), 400

    # Build line items & total
    total_price = 0.0
    line_items = []
    for i, book_id in enumerate(book_ids):
        book_obj = next((b for b in books if b.id == book_id), None)
        qty = quantities[i]
        if not book_obj:
            return jsonify({"error": f"Book {book_id} not found"}), 400
        cost = (book_obj.price or 0.0) * qty
        total_price += cost
        line_items.append({
            "book_id": book_obj.id,
            "title": book_obj.title,
            "book_price": book_obj.price or 0.0,
            "quantity": qty
        })

    # Create invoice
    from models import Invoice, InvoiceItem
    invoice = Invoice(
        user_id=user.id,
        created_at=datetime.utcnow(),
        total_price=total_price
    )
    db.session.add(invoice)
    db.session.commit()

    # Create invoice items
    invoice_items = []
    for li in line_items:
        ii = InvoiceItem(
            invoice_id=invoice.id,
            book_id=li["book_id"],
            book_price=li["book_price"],
            quantity=li["quantity"]
        )
        db.session.add(ii)
        invoice_items.append(ii)

    db.session.commit()

    # Build response
    result = {
        "id": invoice.id,
        "user_name": user.username,
        "created_at": invoice.created_at.isoformat(),
        "total_price": invoice.total_price,
        "items": line_items
    }
    return jsonify(result), 201


@invoices_bp.route("/invoices", methods=["GET"])
@jwt_required()
def list_invoices():
    """
    Returns all invoices for the current logged-in user.
    Example output: [{id, created_at, total_price}, ...]
    """
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401

    invoices = Invoice.query.filter_by(user_id=user.id).order_by(Invoice.created_at.desc()).all()
    data = []
    for inv in invoices:
        data.append({
            "id": inv.id,
            "created_at": inv.created_at.isoformat(),
            "total_price": inv.total_price
        })
    return jsonify(data), 200

@invoices_bp.route("/invoices/<int:invoice_id>", methods=["GET"])
@jwt_required()
def get_invoice(invoice_id):
    """
    Returns details of a single invoice, including line items.
    """
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401

    invoice = Invoice.query.get(invoice_id)
    if not invoice or invoice.user_id != user.id:
        return jsonify({"error": "Invoice not found or not yours"}), 404

    # Build line items
    line_items = []
    for it in invoice.items:
        line_items.append({
            "book_id": it.book_id,
            "book_price": it.book_price,
            "quantity": it.quantity
        })

    result = {
        "id": invoice.id,
        "created_at": invoice.created_at.isoformat(),
        "total_price": invoice.total_price,
        "items": line_items
    }
    return jsonify(result), 200
