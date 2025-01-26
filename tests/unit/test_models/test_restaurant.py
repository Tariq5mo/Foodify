#!/usr/bin/python3
"""Unit tests for Restaurant class"""
import unittest
from unittest.mock import patch
from models.restaurant import Restaurant


class TestRestaurant(unittest.TestCase):
    """Test cases for Restaurant model"""

    def setUp(self):
        """Set up test cases"""
        self.restaurant = Restaurant(
            name="Test Restaurant", city="Test City"
        )

    def test_init_with_required_attributes(self):
        """Test initialization with required attributes"""
        self.assertEqual(self.restaurant.name, "Test Restaurant")
        self.assertEqual(self.restaurant.city, "Test City")
        self.assertIsNone(self.restaurant.logo_url)

    def test_init_with_all_attributes(self):
        """Test initialization with all attributes"""
        restaurant = Restaurant(
            name="Test Restaurant",
            city="Test City",
            logo_url="http://example.com/logo.jpg",
        )
        self.assertEqual(restaurant.logo_url, "http://example.com/logo.jpg")

    def test_str_representation(self):
        """Test string representation"""
        self.restaurant.id = "test123"
        string = str(self.restaurant)
        self.assertIn("[Restaurant] (test123)", string)
        self.assertIn("Test Restaurant", string)
        self.assertIn("Test City", string)

    def test_to_dict_method(self):
        """Test dictionary representation"""
        restaurant_dict = self.restaurant.to_dict()

        self.assertEqual(restaurant_dict["name"], "Test Restaurant")
        self.assertEqual(restaurant_dict["city"], "Test City")
        self.assertEqual(restaurant_dict["__class__"], "Restaurant")
        self.assertIn("id", restaurant_dict)
        self.assertIn("created_at", restaurant_dict)
        self.assertIn("updated_at", restaurant_dict)

    @patch("models.storage")
    def test_save_method(self, mock_storage):
        """Test save method"""
        old_updated_at = self.restaurant.updated_at
        self.restaurant.save()

        self.assertNotEqual(old_updated_at, self.restaurant.updated_at)
        mock_storage.new.assert_called_once_with(self.restaurant)
        mock_storage.save.assert_called_once()

    @patch("models.storage")
    def test_delete_method(self, mock_storage):
        """Test delete method"""
        self.restaurant.delete()
        mock_storage.delete.assert_called_once_with(self.restaurant)

    def test_relationships(self):
        """Test relationship attributes exist"""
        self.assertTrue(hasattr(self.restaurant, "reviews"))
        self.assertTrue(hasattr(self.restaurant, "menu_items"))


if __name__ == "__main__":
    unittest.main()
