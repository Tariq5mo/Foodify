#!/usr/bin/python3
"""Unit tests for welcome routes"""
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_login import LoginManager, UserMixin
from routes.welcome import welcome_routes
from models.menu_item import MenuItem
from models.restaurant import Restaurant
from decimal import Decimal


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id


class TestWelcomeRoutes(unittest.TestCase):
    """Test cases for welcome routes"""

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
            "routes.welcome.render_template", return_value=""
        )
        self.mock_render = self.render_patch.start()

        # Register blueprint
        self.app.register_blueprint(welcome_routes)

        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        """Clean up after tests"""
        self.ctx.pop()
        self.render_patch.stop()

    def test_welcome_page_render(self):
        """Test welcome page rendering"""
        response = self.client.get("/welcome")
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_with(
            "welcome.html", title="Welcome to Foodify"
        )

    def test_root_route(self):
        """Test root route redirects to welcome"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_with(
            "welcome.html", title="Welcome to Foodify"
        )

    @patch("routes.welcome.storage")
    def test_search_meals_no_filters(self, mock_storage):
        """Test meal search without filters"""
        mock_session = MagicMock()
        mock_restaurant = Restaurant(name="Test Restaurant")
        mock_menu_items = [
            MenuItem(
                id="item1",
                name="Test Item 1",
                price=Decimal("10.99"),
                is_available=True,
                restaurant=mock_restaurant,
                image_url="test1.jpg",
            ),
            MenuItem(
                id="item2",
                name="Test Item 2",
                price=Decimal("12.99"),
                is_available=True,
                restaurant=mock_restaurant,
                image_url="test2.jpg",
            ),
        ]
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.count.return_value = 2
        mock_query.limit.return_value.offset.return_value.all.return_value = (
            mock_menu_items
        )
        mock_session.query.return_value = mock_query
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.get("/api/v1/search")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["meals"]), 2)
        self.assertEqual(response.json["total"], 2)

    @patch("routes.welcome.storage")
    def test_search_meals_with_query(self, mock_storage):
        """Test meal search with query parameter"""
        mock_session = MagicMock()
        mock_restaurant = Restaurant(name="Test Restaurant")
        mock_menu_item = MenuItem(
            id="item1",
            name="Burger",
            price=Decimal("10.99"),
            is_available=True,
            restaurant=mock_restaurant,
            image_url="burger.jpg",
        )
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.limit.return_value.offset.return_value.all.return_value = [
            mock_menu_item
        ]
        mock_session.query.return_value = mock_query
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.get("/api/v1/search?query=burger")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["meals"]), 1)
        self.assertEqual(response.json["meals"][0]["name"], "Burger")

    @patch("routes.welcome.storage")
    def test_search_meals_with_restaurant_filter(self, mock_storage):
        """Test meal search with restaurant filter"""
        mock_session = MagicMock()
        mock_restaurant = Restaurant(name="Burger Place")
        mock_menu_item = MenuItem(
            id="item1",
            name="Burger",
            price=Decimal("10.99"),
            is_available=True,
            restaurant=mock_restaurant,
            image_url="burger.jpg",
        )
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.limit.return_value.offset.return_value.all.return_value = [
            mock_menu_item
        ]
        mock_session.query.return_value = mock_query
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.get("/api/v1/search?restaurant=Burger+Place")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["meals"]), 1)
        self.assertEqual(
            response.json["meals"][0]["restaurant_name"], "Burger Place"
        )

    @patch("routes.welcome.storage")
    def test_search_meals_error_handling(self, mock_storage):
        """Test search error handling"""
        mock_storage.session_scope.side_effect = Exception("Database error")

        response = self.client.get("/api/v1/search")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json["error"], "Internal server error")


if __name__ == "__main__":
    unittest.main()
