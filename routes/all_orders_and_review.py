from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required
from models import storage
from models.order import Order
from models.review import Review
from models.restaurant import Restaurant

review_routes = Blueprint("review_routes", __name__)

@review_routes.route("/all_orders_and_review")
@login_required
def all_orders_and_review():
    """Display all orders and review page"""
    try:
        # Get all orders for current user
        user_orders = []
        orders = storage.all(Order).values()
        for order in orders:
            if order.client_id == current_user.id:
                user_orders.append(order)

        # Get all restaurants for reviews
        restaurants = storage.all(Restaurant).values()
        
        return render_template("all_orders_and_review.html", 
                            orders=user_orders,
                            restaurants=restaurants)
                            
    except Exception as e:
        storage.rollback()
        return jsonify({'error': str(e)}), 500

@review_routes.route("/api/v1/submit_review", methods=["POST"])
@login_required
def submit_review():
    """Handle review submission"""
    try:
        data = request.get_json()
        restaurant_name = data.get('restaurant')
        rating = data.get('rating')
        feedback = data.get('feedback')

        # Validate input
        if not all([restaurant_name, rating, feedback]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Find restaurant
        restaurant = None
        restaurants = storage.all(Restaurant).values()
        for rest in restaurants:
            if rest.name == restaurant_name:
                restaurant = rest
                break

        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404

        # Create new review
        review = Review(
            client_id=current_user.id,
            restaurant_id=restaurant.id,
            rating=rating,
            comment=feedback
        )
        storage.new(review)
        storage.save()

        return jsonify({
            'success': True,
            'message': 'Review submitted successfully'
        })

    except Exception as e:
        storage.rollback()
        return jsonify({'error': str(e)}), 500
