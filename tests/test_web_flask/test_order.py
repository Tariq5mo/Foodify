#!/usr/bin/python3
"""Unit tests for order routes"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from routes.order import order_routes
from models.order import Order
from models.order_item import OrderItem
from models.menu_item import MenuItem
from decimal import Decimal


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id


class TestOrderRoutes(unittest.TestCase):
    """Test cases for order routes"""

    def setUp(self):
        """Set up test environment"""
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["LOGIN_DISABLED"] = True  # Disable login requirement
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
            "routes.order.render_template", return_value=""
        )
        self.mock_render = self.render_patch.start()

        # Mock login_required more effectively
        self.login_patch = patch("routes.order.login_required", lambda x: x)
        self.login_patch.start()

        # Register blueprints
        from routes.welcome import welcome_routes  # Add this

        self.app.register_blueprint(welcome_routes)  # Add this
        self.app.register_blueprint(order_routes)

        # Create test client
        self.client = self.app.test_client()

        # Setup request context
        self.ctx = self.app.test_request_context()
        self.ctx.push()

        # Login the user
        login_user(self.mock_user)

    def tearDown(self):
        """Clean up after tests"""
        self.ctx.pop()
        self.login_patch.stop()
        self.render_patch.stop()

    @patch("routes.order.current_user", new_callable=PropertyMock)
    @patch("routes.order.storage")
    def test_update_cart_increase(self, mock_storage, mock_current_user):
        """Test increasing item quantity in cart"""
        mock_current_user.return_value = self.mock_user

        # Mock the menu item
        mock_menu_item = MenuItem(
            id="test_item_id",
            name="Test Item",
            price=Decimal("10.99"),
            is_available=True,
        )

        # Mock the session query
        mock_session = MagicMock()
        mock_session.query.return_value.get.return_value = mock_menu_item

        # Mock active order
        mock_order = Order(
            id="test_order_id",
            client_id=self.mock_user.id,
            status="active",
            total_price=Decimal("0"),
        )
        mock_order.order_items = []

        mock_session.query.return_value.filter_by.return_value.options.return_value.first.return_value = (
            mock_order
        )
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        test_data = {"menu_item_id": "test_item_id", "action": "increase"}

        response = self.client.post(
            "/api/v1/cart/update",
            json=test_data,
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("routes.order.current_user", new_callable=PropertyMock)
    @patch("routes.order.storage")
    def test_get_cart_state(self, mock_storage, mock_current_user):
        """Test getting cart state"""
        mock_current_user.return_value = self.mock_user
        with self.client as c:
            response = c.get("/api/v1/cart/state")
            self.assertEqual(response.status_code, 200)

    @patch("routes.order.current_user", new_callable=PropertyMock)
    @patch("routes.order.storage")
    def test_confirm_order(self, mock_storage, mock_current_user):
        """Test order confirmation"""
        mock_current_user.return_value = self.mock_user
        mock_session = MagicMock()

        # Mock active order with items
        mock_order = Order(
            id="test_order_id",
            client_id=self.mock_user.id,
            status="active",
            total_price=Decimal("21.98"),
        )
        mock_order.order_items = [
            OrderItem(menu_item_id="item1", quantity=2),
            OrderItem(menu_item_id="item2", quantity=1),
        ]

        # Setup session mock
        mock_session.query.return_value.filter_by.return_value.options.return_value.first.return_value = (
            mock_order
        )
        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.post("/confirm_order")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json.get("success"))
        self.assertIn("welcome", response.json.get("redirect", ""))

    @patch("routes.order.current_user", new_callable=PropertyMock)
    @patch("routes.order.storage")
    def test_order_page_render(self, mock_storage, mock_current_user):
        """Test order page rendering"""
        mock_current_user.return_value = self.mock_user
        with self.client as c:
            response = c.get("/order")
            self.assertEqual(response.status_code, 200)

    @patch("routes.order.current_user", new_callable=PropertyMock)
    @patch("routes.order.storage")
    def test_get_cart_state(self, mock_storage, mock_current_user):
        """Test getting cart state"""
        mock_current_user.return_value = self.mock_user

        # Mock active order with items
        mock_order = Order(
            id="test_order_id",
            client_id=self.mock_user.id,
            status="active",
            total_price=Decimal("21.98"),
        )
        mock_order_items = [
            OrderItem(menu_item_id="item1", quantity=2),
            OrderItem(menu_item_id="item2", quantity=1),
        ]
        mock_order.order_items = mock_order_items

        mock_storage.all.return_value = {"Order.test_order": mock_order}

        response = self.client.get("/api/v1/cart/state")
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.json)
        self.assertIn("order", response.json)

    @patch("routes.order.current_user", new_callable=PropertyMock)
    @patch("routes.order.storage")
    def test_confirm_order(self, mock_storage, mock_current_user):
        """Test order confirmation"""
        mock_current_user.return_value = self.mock_user
        mock_session = MagicMock()

        # Mock active order
        mock_order = MagicMock()
        mock_order.total_price = Decimal("21.98")
        mock_session.query.return_value.filter_by.return_value.options.return_value.first.return_value = (
            mock_order
        )

        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.post("/confirm_order")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])

    @patch("routes.order.current_user", new_callable=PropertyMock)
    @patch("routes.order.storage")
    def test_order_page_render(self, mock_storage, mock_current_user):
        """Test order page rendering"""
        mock_current_user.return_value = self.mock_user
        mock_session = MagicMock()

        # Mock active order with items
        mock_menu_item = MenuItem(
            id="test_item_id",
            name="Test Item",
            price=Decimal("10.99"),
            image_url="test.jpg",
        )
        mock_order_item = OrderItem(menu_item=mock_menu_item, quantity=2)
        mock_order = MagicMock()
        mock_order.order_items = [mock_order_item]

        mock_session.query.return_value.filter_by.return_value.options.return_value.first.return_value = (
            mock_order
        )

        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.get("/order")
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_once()


if __name__ == "__main__":
    unittest.main()
