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
    Also returns the user's role so the frontend can know if they're admin.
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

    return jsonify({
        "access_token": access_token,
        "role": user.role   # <--- Return the role as well
    }), 200


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


@users_bp.route("/make_admin/<int:user_id>", methods=["PUT"])
@jwt_required()
def make_user_admin(user_id):
    """
    Convert a normal user to be an admin.
    Must be called by an existing admin.
    Example: PUT /api/make_admin/<user_id>
    """
    acting_user = current_user()
    if not acting_user or not is_admin(acting_user):
        return jsonify({"error": "Admin permission required"}), 403

    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({"error": f"No user found with id={user_id}"}), 404

    if target_user.role == "admin":
        return jsonify({"message": f"User '{target_user.username}' is already an admin"}), 200

    # Update the role
    target_user.role = "admin"
    db.session.commit()

    # Notify that the user is now an admin
    return jsonify({
        "message": f"User '{target_user.username}' is now an admin",
        "user_id": target_user.id,
        "role": target_user.role
    }), 200


@users_bp.route("/demote_admin/<int:user_id>", methods=["PUT"])
@jwt_required()
def demote_user_from_admin(user_id):
    """
    Convert an admin user back to normal user.
    Must be called by an existing admin, or you could require even higher privileges.
    Example: PUT /api/demote_admin/<user_id>
    """
    acting_user = current_user()
    if not acting_user or not is_admin(acting_user):
        return jsonify({"error": "Admin permission required"}), 403

    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({"error": f"No user found with id={user_id}"}), 404

    if target_user.role != "admin":
        return jsonify({"message": f"User '{target_user.username}' is not an admin"}), 200

    # Update the role to normal 'user'
    target_user.role = "user"
    db.session.commit()

    # Notify that the user is now demoted
    return jsonify({
        "message": f"User '{target_user.username}' is now a normal user",
        "user_id": target_user.id,
        "role": target_user.role
    }), 200
