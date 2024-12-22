# routes_users.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
from models import db, User
from schemas import UserSchema

users_bp = Blueprint("users", __name__)
user_schema = UserSchema()


@users_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user (username/password).
    Body: {"username": "...", "password": "..."}
    """
    data = request.get_json() or {}
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    username = data["username"]
    password = data["password"]

    # Check if username already exists
    existing = User.query.filter_by(username=username).first()
    if existing:
        return jsonify({"error": "Username already taken"}), 400

    # Create user
    pw_hash = generate_password_hash(password)
    new_user = User(username=username, password_hash=pw_hash, role="user")
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User '{username}' registered successfully."}), 201


@users_bp.route("/login", methods=["POST"])
def login():
    """
    Log in with username, password. Return JWT if valid.
    Body: {"username": "...", "password": "..."}
    """
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create token
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200


def current_user():
    """
    Helper to get the current logged-in user object (by ID).
    Must be called inside a route with @jwt_required().
    """
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(user_id)


def is_admin(user: User) -> bool:
    """Check if the user has role='admin'."""
    return user and user.role == "admin"
