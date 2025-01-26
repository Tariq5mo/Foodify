#!/usr/bin/python3
"""Unit tests for payment routes"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from routes.payment import payment_routes
from models.order import Order
from models.order_item import OrderItem
from models.menu_item import MenuItem
from decimal import Decimal


class MockUser(UserMixin):
    """Mock user for testing"""

    def __init__(self, user_id):
        self.id = user_id


class TestPaymentRoutes(unittest.TestCase):
    """Test cases for payment routes"""

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
            "routes.payment.render_template", return_value=""
        )
        self.mock_render = self.render_patch.start()

        # Mock login_required
        self.login_patch = patch(
            "routes.payment.login_required", lambda x: x
        )
        self.login_patch.start()

        # Register blueprint
        self.app.register_blueprint(payment_routes)

        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        login_user(self.mock_user)

    def tearDown(self):
        """Clean up after tests"""
        self.ctx.pop()
        self.login_patch.stop()
        self.render_patch.stop()

    @patch("routes.payment.current_user", new_callable=PropertyMock)
    @patch("routes.payment.storage")
    def test_payment_page_no_order(self, mock_storage, mock_current_user):
        """Test payment page rendering with no active order"""
        mock_current_user.return_value = self.mock_user
        mock_storage.all.return_value = {}

        response = self.client.get("/payment")
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_with(
            "payment.html", subtotal="0.00", total="5.00", items=[]
        )

    @patch("routes.payment.current_user", new_callable=PropertyMock)
    @patch("routes.payment.storage")
    def test_payment_page_with_order(self, mock_storage, mock_current_user):
        """Test payment page rendering with active order"""
        mock_current_user.return_value = self.mock_user

        # Mock active order
        mock_order = Order(
            id="test_order_id",
            client_id=self.mock_user.id,
            status="active",
            total_price=Decimal("21.98"),
        )

        # Mock order items
        mock_menu_item = MenuItem(
            id="test_item_id", name="Test Item", price=Decimal("10.99")
        )
        mock_order_item = OrderItem(menu_item_id="test_item_id", quantity=2)
        mock_order.order_items = [mock_order_item]

        mock_storage.all.return_value = {"Order.test_order": mock_order}
        mock_storage.get.return_value = mock_menu_item

        response = self.client.get("/payment")
        self.assertEqual(response.status_code, 200)
        self.mock_render.assert_called_once()

    @patch("routes.payment.current_user", new_callable=PropertyMock)
    @patch("routes.payment.storage")
    def test_get_totals(self, mock_storage, mock_current_user):
        """Test getting order totals"""
        mock_current_user.return_value = self.mock_user
        mock_session = MagicMock()

        # Mock active order with total price
        mock_order = MagicMock()
        mock_order.total_price = Decimal("21.98")
        mock_session.query.return_value.filter_by.return_value.options.return_value.first.return_value = (
            mock_order
        )

        mock_storage.session_scope.return_value.__enter__.return_value = (
            mock_session
        )

        response = self.client.get("/api/v1/payment/totals")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])
        self.assertEqual(response.json["subtotal"], "21.98")
        self.assertEqual(response.json["delivery_fee"], "5.00")
        self.assertEqual(response.json["total"], "26.98")

    def test_apply_valid_coupon(self):
        """Test applying a valid coupon code"""
        test_data = {"code": "WELCOME20"}

        response = self.client.post(
            "/api/v1/apply_coupon",
            json=test_data,
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])
        self.assertEqual(response.json["discount"], 20)

    def test_apply_invalid_coupon(self):
        """Test applying an invalid coupon code"""
        test_data = {"code": "INVALID"}

        response = self.client.post(
            "/api/v1/apply_coupon",
            json=test_data,
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json["success"])
        self.assertEqual(response.json["error"], "Invalid coupon code")


if __name__ == "__main__":
    unittest.main()
