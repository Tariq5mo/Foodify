from flask import Blueprint, render_template

restaurant_routes = Blueprint('restaurant_routes', __name__)


@restaurant_routes.route('/restaurants/burger_blast')
def burger_blast():
    """Route handler for Burger Blast restaurant page"""
    return render_template('restaurants/burger_blast.html')
