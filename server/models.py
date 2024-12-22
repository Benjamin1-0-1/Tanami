# models.py

from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="user")  # e.g. 'admin' or 'user'

    def __repr__(self):
        return f"<User {self.username} (role={self.role})>"


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    publisher = db.Column(db.String(255), nullable=True)
    level = db.Column(db.String(50), nullable=True)
    isbn = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Book {self.title[:30]}... (id={self.id})>"


class BookAudit(db.Model):
    __tablename__ = "book_audits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=True)
    action = db.Column(db.String(20), nullable=False)  # CREATE, UPDATE, DELETE
    old_data = db.Column(db.Text, nullable=True)
    new_data = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="changes_made")
    book = db.relationship("Book", backref="change_logs")

    def __repr__(self):
        return f"<BookAudit user_id={self.user_id}, action={self.action}, time={self.timestamp}>"
