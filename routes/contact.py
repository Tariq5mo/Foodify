from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required
from models import storage
from models.review import Review
from models.restaurant import Restaurant


contact_routes = Blueprint('contact_routes', __name__)


@contact_routes.route("/contact")
def contact():
    """Render contact page with restaurants list"""
    restaurants = storage.all(Restaurant).values()
    return render_template("contact.html",
                           title="Contact Us",
                           restaurants=restaurants)


@contact_routes.route("/api/v1/submit_review", methods=["POST"])
@login_required
def submit_review():
    """Handle review submission"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")
        rating = int(data.get("rating"))
        feedback = data.get("feedback")

        # Validate input
        if not all([restaurant_id, rating, feedback]):
            return jsonify({"error": "Missing required fields"}), 400

        if not 1 <= rating <= 5:
            return jsonify({"error": "Invalid rating"}), 400

        # Create new review
        review = Review(
            client_id=current_user.id,
            restaurant_id=restaurant_id,
            rating=rating,
            comment=feedback
        )

        storage.new(review)
        storage.save()

        return jsonify({
            "success": True,
            "message": "Review submitted successfully"
        })

    except Exception as e:
        storage.rollback()
        return jsonify({"error": str(e)}), 500
