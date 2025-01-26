#!/usr/bin/python3
"""Unit tests for login routes"""
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from routes.login import login_routes, logout_routes, order_routes
from models.client import Client
from models.menu_item import MenuItem
from decimal import Decimal


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id
        self.email = "test@example.com"


class TestLoginRoutes(unittest.TestCase):
    """Test cases for login routes"""

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

        # Mock render_template to return error message for invalid login
        def mock_render(*args, **kwargs):
            if "login.html" in args:
                return "Login Unsuccessful"
            return ""

        self.render_patch = patch(
            "routes.login.render_template", side_effect=mock_render
        )
        self.mock_render = self.render_patch.start()

        # Register blueprints
        from routes.welcome import welcome_routes

        self.app.register_blueprint(welcome_routes)
        self.app.register_blueprint(login_routes)
        self.app.register_blueprint(logout_routes)
        self.app.register_blueprint(order_routes)

        self.client = self.app.test_client()

        # Setup request context
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        login_user(self.mock_user)

    def tearDown(self):
        """Clean up after tests"""
        self.ctx.pop()
        self.render_patch.stop()

    @patch("app.bcrypt")  # Change from 'routes.login.bcrypt' to 'app.bcrypt'
    @patch("routes.login.storage")
    def test_login_success(self, mock_storage, mock_bcrypt):
        """Test successful login"""
        mock_client = Client(
            email="test@example.com", password="hashed_password"
        )
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_client
        )
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )
        mock_bcrypt.check_password_hash.return_value = True

        response = self.client.post(
            "/login",
            data={
                "email": "test@example.com",
                "password": "password123",
                "remember": True,
            },
        )
        self.assertEqual(response.status_code, 302)

    @patch("app.bcrypt")
    @patch("routes.login.storage")
    def test_login_invalid_credentials(self, mock_storage, mock_bcrypt):
        """Test login with invalid credentials"""
        # Mock session and client lookup
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = (
            None
        )
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )
        mock_bcrypt.check_password_hash.return_value = False

        with self.client as c:
            response = c.post(
                "/login",
                data={
                    "email": "wrong@example.com",
                    "password": "wrongpass",
                },
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(
                b"Login Unsuccessful" in response.data
                or "Login Unsuccessful"
                in self.mock_render.call_args[1].get("error", "")
            )

    def test_logout(self):
        """Test logout functionality"""
        login_user(self.mock_user)

        # Option 1: Don't follow redirects and just check redirect status
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)  # Check redirect status
        # Check redirect location
        self.assertIn("/welcome", response.headers["Location"])

        # OR Option 2: Mock welcome template render
        def mock_render(*args, **kwargs):
            if "welcome.html" in args:
                return "Welcome Page"
            return ""

        with patch(
            "routes.welcome.render_template", side_effect=mock_render
        ):
            response = self.client.get("/logout", follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    @patch("routes.login.storage")
    @patch("routes.login.current_user")
    def test_add_menu_item_success(self, mock_current_user, mock_storage):
        """Test successful addition of menu item to order"""
        mock_current_user.id = self.mock_user.id
        mock_menu_item = MenuItem(
            id="test_item_id",
            name="Test Item",
            price=Decimal("10.99"),
            is_available=True,
        )
        mock_storage.get.return_value = mock_menu_item

        test_data = {"menu_item_id": "test_item_id", "quantity_change": 1}

        response = self.client.post(
            "/api/v1/orders/add_item", json=test_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["status"], "success"
        )  # Check exact key

    @patch("routes.login.storage")
    @patch("routes.login.current_user")
    def test_add_menu_item_unavailable(
        self, mock_current_user, mock_storage
    ):
        """Test adding unavailable menu item"""
        mock_current_user.id = self.mock_user.id
        mock_menu_item = MenuItem(
            id="test_item_id",
            name="Test Item",
            price=Decimal("10.99"),
            is_available=False,
        )
        mock_storage.get.return_value = mock_menu_item

        test_data = {"menu_item_id": "test_item_id", "quantity_change": 1}

        response = self.client.post(
            "/api/v1/orders/add_item", json=test_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Item not available")


if __name__ == "__main__":
    unittest.main()
