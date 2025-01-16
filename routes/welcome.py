"""Signup route handler"""

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)
from models import storage
from sqlalchemy.orm import joinedload
from models.menu_item import MenuItem  # Add imports at top

# from app import foodify_app

welcome_routes = Blueprint("welcome_routes", __name__)


@welcome_routes.route("/")
@welcome_routes.route("/welcome")
def welcome():
    return render_template("welcome.html", title="Welcome to Foodify")


@welcome_routes.route("/api/v1/search", methods=["GET"])
def search_meals():
    """Search meals endpoint with proper error handling"""
    try:
        with storage.session_scope() as db_session:  # Use context manager
            query_param = request.args.get("query", "").strip().lower()
            restaurant = request.args.get("restaurant", "All").strip()
            page = int(request.args.get("page", 1))
            per_page = 8

            # Build query with proper session
            query = db_session.query(MenuItem).options(
                joinedload("restaurant")
            )

            # Apply filters
            if query_param:
                query = query.filter(MenuItem.name.ilike(f"%{query_param}%"))
            if restaurant != "All":
                from models.restaurant import Restaurant
                query = query.join(MenuItem.restaurant).filter(
                    Restaurant.name == restaurant
                )

            # Get total count and paginate
            total = query.count()
            paginated_meals = (
                query.limit(per_page).offset((page - 1) * per_page).all()
            )

            return jsonify(
                {
                    "meals": [
                        {
                            "id": str(meal.id),
                            "name": meal.name,
                            "price": float(meal.price),
                            "is_available": meal.is_available,
                            "restaurant_name": meal.restaurant.name,
                            "image_name": meal.image_url,
                        }
                        for meal in paginated_meals
                    ],
                    "total": total,
                }
            )

    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({"error": "Internal server error"}), 500
