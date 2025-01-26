#!/usr/bin/python3
"""Unit tests for delivery routes"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from routes.delivery import delivery_routes
from models.client import Client


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id


class TestDeliveryRoutes(unittest.TestCase):
    """Test cases for delivery routes"""

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
            "routes.delivery.render_template", return_value=""
        )
        self.mock_render = self.render_patch.start()

        self.app.register_blueprint(delivery_routes)
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

    @patch("routes.delivery.current_user", new_callable=PropertyMock)
    @patch("routes.delivery.storage")
    def test_delivery_page_render(self, mock_storage, mock_current_user):
        """Test delivery page rendering with stored location"""
        mock_current_user.return_value = self.mock_user
        mock_session = MagicMock()
        mock_client = Client(
            id="test_user_id",
            address="123 Test St",
            latitude=40.7128,
            longitude=-74.0060,
        )
        mock_session.query.return_value.get.return_value = mock_client
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.get("/delivery")

        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_with(
            "delivery.html",
            stored_location={
                "address": "123 Test St",
                "lat": 40.7128,
                "lng": -74.0060,
            },
        )

    @patch("routes.delivery.current_user", new_callable=PropertyMock)
    @patch("routes.delivery.storage")
    def test_delivery_page_no_location(
        self, mock_storage, mock_current_user
    ):
        """Test delivery page rendering without stored location"""
        mock_current_user.return_value = self.mock_user
        mock_session = MagicMock()
        mock_client = Client(id="test_user_id")
        mock_session.query.return_value.get.return_value = mock_client
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.get("/delivery")

        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_with(
            "delivery.html", stored_location=None
        )

    @patch("routes.delivery.current_user", new_callable=PropertyMock)
    @patch("routes.delivery.storage")
    def test_save_location_success(self, mock_storage, mock_current_user):
        """Test successful location save"""
        mock_current_user.return_value = self.mock_user
        mock_session = MagicMock()
        mock_client = Client(id="test_user_id")
        mock_session.query.return_value.get.return_value = mock_client
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        test_data = {
            "lat": 40.7128,
            "lng": -74.0060,
            "address": "123 Test St",
            "phone": "1234567890",
            "instructions": "Leave at door",
        }

        response = self.client.post("/api/v1/location/save", json=test_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

    @patch("routes.delivery.current_user", new_callable=PropertyMock)
    @patch("routes.delivery.storage")
    def test_save_location_error(self, mock_storage, mock_current_user):
        """Test location save with database error"""
        mock_current_user.return_value = self.mock_user
        mock_session = MagicMock()
        mock_session.commit.side_effect = Exception("Database error")
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        test_data = {
            "lat": 40.7128,
            "lng": -74.0060,
            "address": "123 Test St",
            "phone": "1234567890",
        }

        response = self.client.post("/api/v1/location/save", json=test_data)

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)


if __name__ == "__main__":
    unittest.main()
