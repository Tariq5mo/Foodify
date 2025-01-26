#!/usr/bin/python3
"""Unit tests for signup routes"""
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_login import LoginManager, UserMixin
from routes.signup import signup_routes
from models.client import Client


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id
        self.email = "test@example.com"


class TestSignupRoutes(unittest.TestCase):
    """Test cases for signup routes"""

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
            "routes.signup.render_template", return_value=""
        )
        self.mock_render = self.render_patch.start()

        # Register blueprints
        from routes.welcome import welcome_routes
        from routes.login import login_routes  # Add this

        self.app.register_blueprint(welcome_routes)
        self.app.register_blueprint(signup_routes)
        self.app.register_blueprint(login_routes)  # Add this

        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        """Clean up after tests"""
        self.ctx.pop()
        self.render_patch.stop()

    def test_signup_page_render(self):
        """Test signup page rendering"""
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_with(
            "signup.html", title="Sign Up", form=unittest.mock.ANY
        )

    @patch("app.bcrypt")
    @patch("routes.signup.storage")
    def test_signup_success(self, mock_storage, mock_bcrypt):
        """Test successful signup"""
        mock_session = MagicMock()
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )
        mock_bcrypt.generate_password_hash.return_value = b"hashed_password"

        test_data = {
            "username": "testuser",
            "email": "newuser@example.com",
            "password": "Test123@pass",
            "address": "123 Test St",
        }

        response = self.client.post("/signup", data=test_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertIn("/login", response.headers["Location"])
        mock_storage.new.assert_called_once()
        mock_storage.save.assert_called_once()

    @patch("routes.signup.storage")
    def test_signup_existing_username(self, mock_storage):
        """Test signup with existing username"""
        # Mock existing user check
        existing_client = Client(
            username="testuser", email="existing@example.com"
        )
        mock_storage.all.return_value = {"Client.1": existing_client}

        test_data = {
            "username": "testuser",  # Existing username
            "email": "new@example.com",
            "password": "Test123@pass",
            "address": "123 Test St",
        }

        response = self.client.post("/signup", data=test_data)
        self.assertEqual(response.status_code, 200)  # Stay on signup page
        self.mock_render.assert_called_with(
            "signup.html", title="Sign Up", form=unittest.mock.ANY
        )

    @patch("routes.signup.storage")
    def test_signup_existing_email(self, mock_storage):
        """Test signup with existing email"""
        # Mock existing email check
        existing_client = Client(
            username="existinguser", email="test@example.com"
        )
        mock_storage.all.return_value = {"Client.1": existing_client}

        test_data = {
            "username": "newuser",
            "email": "test@example.com",  # Existing email
            "password": "Test123@pass",
            "address": "123 Test St",
        }

        response = self.client.post("/signup", data=test_data)
        self.assertEqual(response.status_code, 200)  # Stay on signup page
        self.mock_render.assert_called_with(
            "signup.html", title="Sign Up", form=unittest.mock.ANY
        )

    def test_signup_invalid_password(self):
        """Test signup with invalid password format"""
        test_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "weak",  # Invalid password
            "address": "123 Test St",
        }

        response = self.client.post("/signup", data=test_data)
        self.assertEqual(response.status_code, 200)  # Stay on signup page
        self.mock_render.assert_called_with(
            "signup.html", title="Sign Up", form=unittest.mock.ANY
        )

    @patch("routes.signup.current_user")
    def test_signup_authenticated_user(self, mock_current_user):
        """Test signup attempt by already authenticated user"""
        mock_current_user.is_authenticated = True

        response = self.client.get("/signup")
        self.assertEqual(
            response.status_code, 302
        )  # Redirect to welcome page
        self.assertIn("/welcome", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()
