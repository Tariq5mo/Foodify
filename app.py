#!/usr/bin/env python3
"""The Foodify app
"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import storage


# Create Flask app instance first
foodify_app = Flask(__name__, template_folder="templates")
foodify_app.config["SECRET_KEY"] = (
    "0e12c1e7483fe5a5e0088620aa95b29d265213904ca0fb375d558ab9ceaa4991"
)

# Initialize login manager before importing routes
login_manager = LoginManager(foodify_app)
login_manager.login_view = "login_routes.login"  # Updated this line
login_manager.login_message_category = "info"
bcrypt = Bcrypt(foodify_app)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    from models import storage
    from models.client import Client

    # Get all clients and find the one with matching ID
    clients = storage.all(Client).values()
    for client in clients:
        if client.id == user_id:
            return client
    return None


def close_db(e=None):
    """Cleanup function to be called after each request"""
    storage.close()


# Import routes after login_manager is initialized
from routes.login import login_routes, logout_routes
from routes.user_setting import setting_routes
from routes.signup import signup_routes
from routes.welcome import welcome_routes
from routes.order import order_routes
from routes.payment import payment_routes
from routes.all_orders_and_review import review_routes
from routes.delivery import delivery_routes  # Changed from location_routes

# Register blueprints
foodify_app.register_blueprint(login_routes)
foodify_app.register_blueprint(logout_routes)
foodify_app.register_blueprint(setting_routes)
foodify_app.register_blueprint(signup_routes)
foodify_app.register_blueprint(welcome_routes)
foodify_app.register_blueprint(order_routes)
foodify_app.register_blueprint(payment_routes)
foodify_app.register_blueprint(review_routes)
foodify_app.register_blueprint(delivery_routes)  # Changed from location_routes

# Register cleanup function with Flask app
foodify_app.teardown_appcontext(close_db)

if __name__ == "__main__":
    foodify_app.run(debug=True)
