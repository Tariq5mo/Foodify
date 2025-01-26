#!/usr/bin/python3
"""Unit tests for MenuItem class"""
import unittest
from unittest.mock import patch
from models.menu_item import MenuItem


class TestMenuItem(unittest.TestCase):
    """Test cases for MenuItem class"""

    def setUp(self):
        """Set up test cases"""
        self.menu_item = MenuItem(
            restaurant_id="test-restaurant-id",
            name="Test Item",
            price=9.99,
            is_available=True,
        )

    def test_init_with_required_attributes(self):
        """Test initialization with required attributes"""
        self.assertEqual(self.menu_item.restaurant_id, "test-restaurant-id")
        self.assertEqual(self.menu_item.name, "Test Item")
        self.assertEqual(float(self.menu_item.price), 9.99)
        self.assertTrue(self.menu_item.is_available)

    def test_init_with_optional_attributes(self):
        """Test initialization with optional attributes"""
        menu_item = MenuItem(
            restaurant_id="test-restaurant-id",
            name="Test Item",
            price=9.99,
            is_available=True,
            image_url="http://example.com/image.jpg",
        )
        self.assertEqual(menu_item.image_url, "http://example.com/image.jpg")

    @patch("models.storage")
    def test_save_method(self, mock_storage):
        """Test save method"""
        self.menu_item.save()
        mock_storage.new.assert_called_once_with(self.menu_item)
        mock_storage.save.assert_called_once()

    def test_to_dict_method(self):
        """Test dictionary representation"""
        menu_dict = self.menu_item.to_dict()

        self.assertEqual(menu_dict["restaurant_id"], "test-restaurant-id")
        self.assertEqual(menu_dict["name"], "Test Item")
        self.assertEqual(float(menu_dict["price"]), 9.99)
        self.assertTrue(menu_dict["is_available"])
        self.assertEqual(menu_dict["__class__"], "MenuItem")

    def test_str_representation(self):
        """Test string representation"""
        string = str(self.menu_item)
        self.assertIn("MenuItem", string)
        self.assertIn(self.menu_item.id, string)
        self.assertIn(self.menu_item.name, string)

    @patch("models.storage")
    def test_delete_method(self, mock_storage):
        """Test delete method"""
        self.menu_item.delete()
        mock_storage.delete.assert_called_once_with(self.menu_item)


if __name__ == "__main__":
    unittest.main()
