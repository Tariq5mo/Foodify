#!/usr/bin/python3
"""Unit tests for restaurant routes"""
import unittest
from unittest.mock import patch
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from routes.restaurant import restaurant_routes


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id


class TestRestaurantRoutes(unittest.TestCase):
    """Test cases for restaurant routes"""

    def setUp(self):
        """Set up test environment"""
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["LOGIN_DISABLED"] = True
        self.app.secret_key = "test_secret_key"

        # Initialize LoginManager
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        # Create mock user
        self.mock_user = MockUser("test_user_id")

        @self.login_manager.user_loader
        def load_user(user_id):
            return self.mock_user

        # Mock render_template
        self.render_patch = patch(
            "routes.restaurant.render_template", return_value=""
        )
        self.mock_render = self.render_patch.start()

        # Register blueprint
        self.app.register_blueprint(restaurant_routes)

        # Create test client
        self.client = self.app.test_client()

        # Setup request context
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        login_user(self.mock_user)

    def tearDown(self):
        """Clean up after tests"""
        self.ctx.pop()
        self.render_patch.stop()

    def test_burger_blast_page_render(self):
        """Test Burger Blast restaurant page rendering"""
        response = self.client.get("/restaurants/burger_blast")
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_once_with(
            "restaurants/burger_blast.html"
        )

    @patch("routes.restaurant.render_template")
    def test_burger_blast_template_variables(self, mock_render):
        """Test template rendering with correct variables"""
        mock_render.return_value = ""
        self.client.get("/restaurants/burger_blast")

        # Verify template name
        template_name = mock_render.call_args[0][0]
        self.assertEqual(template_name, "restaurants/burger_blast.html")


if __name__ == "__main__":
    unittest.main()
