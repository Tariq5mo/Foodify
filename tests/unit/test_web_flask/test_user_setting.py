#!/usr/bin/python3
"""Unit tests for user setting routes"""
import unittest
from unittest.mock import patch, PropertyMock
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from routes.user_setting import setting_routes
from models.client import Client


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id
        self.username = "testuser"
        self.email = "test@example.com"
        self.address = "123 Test St"


class TestUserSettingRoutes(unittest.TestCase):
    """Test cases for user setting routes"""

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
            "routes.user_setting.render_template", return_value=""
        )
        self.mock_render = self.render_patch.start()

        # Mock login_required
        self.login_patch = patch(
            "routes.user_setting.login_required", lambda x: x
        )
        self.login_patch.start()

        # Mock current_user
        self.user_patch = patch(
            "routes.user_setting.current_user", new=self.mock_user
        )
        self.user_patch.start()

        # Register blueprint
        self.app.register_blueprint(setting_routes)

        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        login_user(self.mock_user)

    def tearDown(self):
        """Clean up after tests"""
        self.ctx.pop()
        self.render_patch.stop()
        self.login_patch.stop()
        self.user_patch.stop()

    def test_setting_page_render(self):
        """Test settings page rendering"""
        response = self.client.get("/setting")
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_with(
            "user_setting.html", user_setting_form=unittest.mock.ANY
        )

    @patch("routes.user_setting.storage")
    @patch("routes.user_setting.current_user", new_callable=PropertyMock)
    def test_update_existing_email(self, mock_current_user, mock_storage):
        """Test update with existing email"""
        mock_current_user.return_value = self.mock_user
        mock_current_user.return_value.email = "current@example.com"
        existing_client = Client(id="other_id", email="existing@example.com")
        mock_storage.all.return_value = {"Client.1": existing_client}

        test_data = {
            "username": "testuser",
            "email": "existing@example.com",
            "address": "123 Test St",
        }

        response = self.client.post("/setting", data=test_data)
        self.assertEqual(response.status_code, 302)
        mock_storage.save.assert_not_called()

    @patch("app.bcrypt")
    @patch("routes.user_setting.storage")
    def test_update_password_incorrect_current(
        self, mock_storage, mock_bcrypt
    ):
        """Test password update with incorrect current password"""
        mock_client = Client(id="test_user_id", password="old_hash")
        mock_storage.all.return_value = {"Client.1": mock_client}
        mock_bcrypt.check_password_hash.return_value = False

        test_data = {
            "username": "testuser",
            "email": "test@example.com",
            "address": "123 Test St",
            "current_password": "wrongpass",
            "new_password": "NewPass123@",
        }

        response = self.client.post("/setting", data=test_data)
        self.assertEqual(response.status_code, 302)
        mock_storage.save.assert_not_called()

    @patch("routes.user_setting.storage")
    def test_user_not_found(self, mock_storage):
        """Test update when user not found in database"""
        mock_storage.all.return_value = {}

        test_data = {
            "username": "testuser",
            "email": "test@example.com",
            "address": "123 Test St",
        }

        response = self.client.post("/setting", data=test_data)
        self.assertEqual(response.status_code, 302)
        mock_storage.save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
