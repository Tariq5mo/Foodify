#!/usr/bin/env python3
"""The Foodify app
"""
from routes.delivery import delivery_routes  # Changed from location_routes
from routes.payment import payment_routes
from routes.order import order_routes
from routes.welcome import welcome_routes
from routes.signup import signup_routes
from routes.user_setting import setting_routes
from routes.contact import contact_routes
from routes.login import login_routes, logout_routes
from routes.restaurant import restaurant_routes
from routes.config import config_routes  # Add this import
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import storage
from dotenv import load_dotenv
import os

load_dotenv()

# Create Flask app instance first
foodify_app = Flask(__name__, template_folder="templates")
foodify_app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

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


# Error handlers
@foodify_app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden error"""
    return render_template('403.html'), 403


@foodify_app.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found error"""
    return render_template('404.html'), 404


@foodify_app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server error"""
    storage.rollback()  # Rollback the session in case of database errors
    return render_template('500.html'), 500


# Import routes after login_manager is initialized


# Register blueprints
foodify_app.register_blueprint(login_routes)
foodify_app.register_blueprint(logout_routes)
foodify_app.register_blueprint(setting_routes)
foodify_app.register_blueprint(signup_routes)
foodify_app.register_blueprint(welcome_routes)
foodify_app.register_blueprint(order_routes)
foodify_app.register_blueprint(payment_routes)
foodify_app.register_blueprint(delivery_routes)  # Changed from location_routes
foodify_app.register_blueprint(contact_routes)
foodify_app.register_blueprint(restaurant_routes)  # Add this line
foodify_app.register_blueprint(config_routes)

# Register cleanup function with Flask app
foodify_app.teardown_appcontext(close_db)

if __name__ == "__main__":
    foodify_app.run(debug=True)
