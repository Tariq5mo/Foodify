#!/usr/bin/python3
"""Unit tests for contact routes"""
import unittest
from unittest.mock import patch, PropertyMock
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from routes.contact import contact_routes
from models.restaurant import Restaurant
from functools import wraps


def mock_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)

    return decorated_function


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id


class TestContactRoutes(unittest.TestCase):
    """Test cases for contact routes"""

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

        # Mock login_required decorator
        self.login_patch = patch("flask_login.login_required", lambda x: x)
        self.login_patch.start()

        # Mock render_template
        self.render_patch = patch(
            "routes.contact.render_template", return_value=""
        )
        self.mock_render = self.render_patch.start()

        # Register blueprint
        self.app.register_blueprint(contact_routes)
        self.client = self.app.test_client()

        # Setup request context
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        login_user(self.mock_user)

    def tearDown(self):
        """Clean up after tests"""
        self.ctx.pop()
        self.login_patch.stop()
        self.render_patch.stop()

    @patch("routes.contact.current_user", new_callable=PropertyMock)
    @patch("routes.contact.storage")
    def test_contact_page_render(self, mock_storage, mock_current_user):
        """Test contact page rendering"""
        mock_current_user.return_value = self.mock_user
        mock_restaurants = [
            Restaurant(
                name="Test Restaurant",
                city="Test City",
                id="test_restaurant_id",
            )
        ]
        mock_storage.all.return_value = {
            f"Restaurant.{r.id}": r for r in mock_restaurants
        }

        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        mock_storage.all.assert_called_once_with(Restaurant)

    @patch("routes.contact.current_user", new_callable=PropertyMock)
    @patch("routes.contact.storage")
    def test_submit_review_success(self, mock_storage, mock_current_user):
        """Test successful review submission"""
        mock_current_user.return_value = self.mock_user

        test_data = {
            "restaurant_id": "test_restaurant_id",
            "rating": 5,
            "feedback": "Great service!",
        }

        with self.client as c:
            response = c.post(
                "/api/v1/submit_review",
                json=test_data,
                headers={"Content-Type": "application/json"},
            )
            self.assertEqual(response.status_code, 200)
            mock_storage.new.assert_called_once()
            mock_storage.save.assert_called_once()

    @patch("routes.contact.current_user", new_callable=PropertyMock)
    def test_submit_review_invalid_rating(self, mock_current_user):
        """Test review submission with invalid rating"""
        mock_current_user.return_value = self.mock_user

        test_data = {
            "restaurant_id": "test_restaurant_id",
            "rating": 6,  # Invalid rating > 5
            "feedback": "Great service!",
        }

        response = self.client.post("/api/v1/submit_review", json=test_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid rating", response.data)

    @patch("routes.contact.current_user", new_callable=PropertyMock)
    @patch("routes.contact.storage")
    def test_submit_review_database_error(
        self, mock_storage, mock_current_user
    ):
        """Test review submission with database error"""
        mock_current_user.return_value = self.mock_user
        mock_storage.save.side_effect = Exception("Database error")

        test_data = {
            "restaurant_id": "test_restaurant_id",
            "rating": 5,
            "feedback": "Great service!",
        }

        response = self.client.post("/api/v1/submit_review", json=test_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Database error", response.data)
        mock_storage.new.assert_called_once()
        mock_storage.save.assert_called_once()
        mock_storage.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
