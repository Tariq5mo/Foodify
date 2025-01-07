#!/usr/bin/env python3
"""The Foodify app
"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Create Flask app instance first
foodify_app = Flask(__name__, template_folder='templates')
foodify_app.config['SECRET_KEY']='0e12c1e7483fe5a5e0088620aa95b29d265213904ca0fb375d558ab9ceaa4991'

# Initialize login manager before importing routes
login_manager = LoginManager(foodify_app)
login_manager.login_view = "login"
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

# Import routes after login_manager is initialized
from routes.login import login_routes
# from routes.login import logout_routes
from routes.signup import signup_routes
from routes.welcome import welcome_routes

# Register blueprints
foodify_app.register_blueprint(login_routes)
foodify_app.register_blueprint(signup_routes)
foodify_app.register_blueprint(welcome_routes)

if __name__ == "__main__":
    foodify_app.run(debug=True)