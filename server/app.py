# app.py

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Basic config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "SUPER-SECRET-KEY"
    app.config["JWT_SECRET_KEY"] = "JWT-SECRET-KEY"

    from models import db  # import the single db instance
    db.init_app(app)

    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    # Optionally, restrict or allow all CORS:
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Import & register your blueprints
    from routes_books import books_bp
    from routes_users import users_bp
    from routes_invoices import invoices_bp

    app.register_blueprint(books_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api")
    app.register_blueprint(invoices_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
