# auth.py
"""
A very simple in-memory user store and helper functions
for user registration and login for demonstration.
In production, you'd store users in the database.
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# In-memory user storage: {username: {"password_hash": "..."}}
users_db = {}


@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user.
    Expects: {"username": "...", "password": "..."}
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    if username in users_db:
        return jsonify({"error": "User already exists"}), 400

    pw_hash = generate_password_hash(password)
    users_db[username] = {"password_hash": pw_hash}
    return jsonify({"message": f"User '{username}' registered."}), 201


@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Login a user.
    Expects: {"username": "...", "password": "..."}
    Returns: {"access_token": "..."}
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user_record = users_db.get(username)
    if not user_record:
        return jsonify({"error": "Invalid username or password"}), 401

    if not check_password_hash(user_record["password_hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    # If valid, create JWT
    token = create_access_token(identity=username)
    return jsonify({"access_token": token}), 200
