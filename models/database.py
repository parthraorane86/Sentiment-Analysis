"""
database.py - Database models and setup using SQLAlchemy ORM
This file defines the Review model and initializes the SQLite database.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a SQLAlchemy instance (will be linked to the Flask app later)
db = SQLAlchemy()


class Review(db.Model):
    """
    Review model - represents a single product review in the database.
    Each row stores the review text, its detected sentiment, product category,
    current resolution status, and the timestamp it was created.
    """
    __tablename__ = "reviews"

    # Primary key - auto-incremented unique ID for each review
    id = db.Column(db.Integer, primary_key=True)

    # The actual review text entered by the user
    review_text = db.Column(db.Text, nullable=False)

    # Sentiment detected: Positive, Negative, or Neutral
    sentiment = db.Column(db.String(20), nullable=False, default="Neutral")

    # Product category detected: Phone, Laptop, Chair, etc.
    category = db.Column(db.String(50), nullable=False, default="Other")

    # Status managed by the admin: Unresolved, Under Process, or Resolved
    status = db.Column(db.String(20), nullable=False, default="Unresolved")

    # Timestamp automatically set when the review is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review id={self.id} sentiment={self.sentiment} category={self.category}>"

    def to_dict(self):
        """Convert the model object to a plain Python dictionary (useful for APIs)."""
        return {
            "id": self.id,
            "review_text": self.review_text,
            "sentiment": self.sentiment,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else "",
        }


def init_db(app):
    """
    Initialize the database with the Flask app.
    Creates all tables if they do not already exist.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("[DB] Database initialized — tables created if not present.")
