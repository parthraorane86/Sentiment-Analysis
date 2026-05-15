"""
app.py - Main Flask Application Entry Point
Complaint Management System

This file:
  - Creates the Flask app
  - Configures the SQLite database
  - Registers all routes (user review page + admin dashboard)
  - Handles form submissions, sentiment analysis, and category detection
"""

import os
import functools
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

# Import database model and initializer
from models.database import db, Review, init_db

# Import utility functions
from utils.sentiment import analyze_sentiment
from utils.category import detect_category

# ---------------------------------------------------------------------------
# APP CONFIGURATION
# ---------------------------------------------------------------------------

app = Flask(__name__)

# Secret key for flash messages / sessions (change this in production!)
app.config["SECRET_KEY"] = "ai-review-system-secret-key-2024"

# ---------------------------------------------------------------------------
# ADMIN CREDENTIALS  (hardcoded for simplicity — use a DB in production)
# ---------------------------------------------------------------------------

ADMIN_USERNAME = "parth"
ADMIN_PASSWORD = "parth"


# ---------------------------------------------------------------------------
# LOGIN REQUIRED DECORATOR  — protects admin-only routes
# ---------------------------------------------------------------------------

def login_required(f):
    """Decorator: redirects to /login if the user is not authenticated."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            flash("🔒 Please log in to access the admin panel.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# SQLite database stored in the project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "reviews.db")

# Disable modification tracking (saves memory, not needed here)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database (creates tables if they don't exist)
init_db(app)


# ---------------------------------------------------------------------------
# ROUTE 1 — USER REVIEW SUBMISSION PAGE  (GET + POST)
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Home page — displays the review submission form.
    On POST: processes the review, saves it to the database,
             and shows the result to the user.
    """

    result = None  # Will hold the analysis result to display

    if request.method == "POST":
        # 1. Get review text from the form
        review_text = request.form.get("review_text", "").strip()

        # 2. Validate: do not allow empty submissions
        if not review_text:
            flash("⚠️ Please enter a review before submitting.", "warning")
            return render_template("index.html", result=None)

        if len(review_text) < 5:
            flash("⚠️ Review is too short. Please write at least 5 characters.", "warning")
            return render_template("index.html", result=None)

        # 3. Analyze sentiment using TextBlob
        sentiment = analyze_sentiment(review_text)

        # 4. Detect product category using keyword matching
        category = detect_category(review_text)

        # 5. Save the review to the SQLite database
        new_review = Review(
            review_text=review_text,
            sentiment=sentiment,
            category=category,
            status="Unresolved"  # Default status for all new reviews
        )
        db.session.add(new_review)
        db.session.commit()

        # 6. Prepare result to display on the page
        result = {
            "review_text": review_text,
            "sentiment": sentiment,
            "category": category,
            "status": "Unresolved",
        }

        flash("✅ Your review has been submitted successfully!", "success")

    return render_template("index.html", result=result)


# ---------------------------------------------------------------------------
# ROUTE 2 — ADMIN DASHBOARD  (GET)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ROUTE: LOGIN / LOGOUT
# ---------------------------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page — accepts GET to show the form and POST to validate credentials.
    On success: sets session flag and redirects to /dashboard.
    On failure: flashes an error and re-renders the login page.
    """
    # Already logged in? Go straight to dashboard
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            session["admin_user"] = username
            flash(f"👋 Welcome back, {username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Invalid username or password. Please try again.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clears the admin session and redirects to the login page."""
    session.clear()
    flash("✅ You have been logged out successfully.", "success")
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# ROUTE 2 — ADMIN DASHBOARD  (GET)  [protected]
# ---------------------------------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    """
    Admin/Operator Dashboard — shows all reviews with filters and search.
    Supports filtering by sentiment, category, and status.
    Also supports keyword search across review text.
    """

    # Collect filter values from the URL query parameters
    filter_sentiment = request.args.get("sentiment", "")
    filter_category  = request.args.get("category", "")
    filter_status    = request.args.get("status", "")
    search_query     = request.args.get("search", "").strip()

    # Start with all reviews, ordered newest first
    query = Review.query.order_by(Review.created_at.desc())

    # Apply filters if provided
    if filter_sentiment:
        query = query.filter(Review.sentiment == filter_sentiment)
    if filter_category:
        query = query.filter(Review.category == filter_category)
    if filter_status:
        query = query.filter(Review.status == filter_status)
    if search_query:
        query = query.filter(Review.review_text.ilike(f"%{search_query}%"))

    reviews = query.all()

    # Gather unique values for filter dropdowns
    all_sentiments = ["Positive", "Negative", "Neutral"]
    all_statuses   = ["Unresolved", "Under Process", "Resolved"]
    all_categories = [
        "Phone", "Laptop", "Chair", "Table", "Headphones",
        "Keyboard", "Mouse", "TV", "Watch", "Camera", "Other"
    ]

    # Dashboard summary stats (using all reviews, ignoring active filters)
    total_reviews   = Review.query.count()
    positive_count  = Review.query.filter_by(sentiment="Positive").count()
    negative_count  = Review.query.filter_by(sentiment="Negative").count()
    neutral_count   = Review.query.filter_by(sentiment="Neutral").count()
    unresolved_count = Review.query.filter_by(status="Unresolved").count()

    return render_template(
        "dashboard.html",
        reviews=reviews,
        all_sentiments=all_sentiments,
        all_statuses=all_statuses,
        all_categories=all_categories,
        filter_sentiment=filter_sentiment,
        filter_category=filter_category,
        filter_status=filter_status,
        search_query=search_query,
        # Stats
        total_reviews=total_reviews,
        positive_count=positive_count,
        negative_count=negative_count,
        neutral_count=neutral_count,
        unresolved_count=unresolved_count,
    )


# ---------------------------------------------------------------------------
# ROUTE 3 — UPDATE REVIEW STATUS  (POST)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ROUTE 3 — UPDATE REVIEW STATUS  (POST)  [protected]
# ---------------------------------------------------------------------------

@app.route("/update_status/<int:review_id>", methods=["POST"])
@login_required
def update_status(review_id):
    """
    Admin action — updates the status of a specific review.
    Called when the operator changes the status dropdown in the dashboard.
    """

    # Find the review by ID, or return 404 if not found
    review = Review.query.get_or_404(review_id)

    # Get the new status from the form submission
    new_status = request.form.get("status", "Unresolved")

    # Validate the status is one of the allowed values
    allowed_statuses = ["Unresolved", "Under Process", "Resolved"]
    if new_status not in allowed_statuses:
        flash("⚠️ Invalid status selected.", "warning")
        return redirect(url_for("dashboard"))

    # Update and save
    review.status = new_status
    db.session.commit()

    flash(f"✅ Review #{review_id} status updated to '{new_status}'.", "success")
    return redirect(url_for("dashboard"))


# ---------------------------------------------------------------------------
# ROUTE 4 — DELETE REVIEW  (POST)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ROUTE 4 — DELETE REVIEW  (POST)  [protected]
# ---------------------------------------------------------------------------

@app.route("/delete_review/<int:review_id>", methods=["POST"])
@login_required
def delete_review(review_id):
    """
    Admin action — permanently deletes a review from the database.
    """
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash(f"🗑️ Review #{review_id} has been deleted.", "info")
    return redirect(url_for("dashboard"))


# ---------------------------------------------------------------------------
# ROUTE 5 — API: GET STATS (JSON)  — Bonus: useful for future charting
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# ROUTE 5 — API: GET STATS (JSON)  [protected]
# ---------------------------------------------------------------------------

@app.route("/api/stats")
@login_required
def api_stats():
    """Returns a JSON summary of review stats — useful for front-end charts."""
    stats = {
        "total":      Review.query.count(),
        "positive":   Review.query.filter_by(sentiment="Positive").count(),
        "negative":   Review.query.filter_by(sentiment="Negative").count(),
        "neutral":    Review.query.filter_by(sentiment="Neutral").count(),
        "unresolved": Review.query.filter_by(status="Unresolved").count(),
        "under_process": Review.query.filter_by(status="Under Process").count(),
        "resolved":   Review.query.filter_by(status="Resolved").count(),
    }
    return jsonify(stats)


# ---------------------------------------------------------------------------
# RUN THE APP
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # host="0.0.0.0" makes the app accessible externally (needed for AWS EC2)
    # debug=True shows errors in browser (turn OFF in production)
    app.run(host="0.0.0.0", port=5000, debug=True)
