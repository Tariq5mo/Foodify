#!/usr/bin/python3
"""Unit tests for Order class"""
import unittest
from unittest.mock import patch
from models.order import Order


class TestOrder(unittest.TestCase):
    """Test cases for Order model"""

    def setUp(self):
        """Set up a basic Order instance"""
        self.order = Order(client_id="test_client", total_price=15.50)

    def test_init_attributes(self):
        """Test initialization of required attributes"""
        self.assertEqual(self.order.client_id, "test_client")
        self.assertEqual(float(self.order.total_price), 15.50)
        # Remove order_date check since it's a database-level default
        # self.assertIsInstance(self.order.order_date, datetime)

    def test_str_representation(self):
        """Test string representation"""
        self.order.id = "test123"
        self.assertIn("[Order] (test123)", str(self.order))

    def test_to_dict_method(self):
        """Test dictionary conversion of Order instance"""
        order_dict = self.order.to_dict()
        self.assertEqual(order_dict["__class__"], "Order")
        self.assertIn("client_id", order_dict)
        self.assertIn("total_price", order_dict)

    @patch("models.storage")
    def test_save_method(self, mock_storage):
        """Test saving an Order"""
        old_updated_at = self.order.updated_at
        self.order.save()
        self.assertNotEqual(old_updated_at, self.order.updated_at)
        mock_storage.new.assert_called_once_with(self.order)
        mock_storage.save.assert_called_once()

    @patch("models.storage")
    def test_delete_method(self, mock_storage):
        """Test deleting an Order"""
        self.order.delete()
        mock_storage.delete.assert_called_once_with(self.order)


if __name__ == "__main__":
    unittest.main()
