#!/usr/bin/python3
"""Unit tests for Review class"""
import unittest
from unittest.mock import patch
from models.review import Review


class TestReview(unittest.TestCase):
    """Test cases for Review model"""

    def setUp(self):
        """Set up test cases"""
        self.review = Review(
            client_id="test_client_id",
            restaurant_id="test_restaurant_id",
            rating=5,
            comment="Great food!",
        )

    def test_init_with_required_attributes(self):
        """Test initialization with required attributes"""
        self.assertEqual(self.review.client_id, "test_client_id")
        self.assertEqual(self.review.restaurant_id, "test_restaurant_id")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Great food!")

    def test_str_representation(self):
        """Test string representation"""
        self.review.id = "test123"
        string = str(self.review)
        self.assertIn("[Review] (test123)", string)
        self.assertIn("test_client_id", string)
        self.assertIn("test_restaurant_id", string)

    def test_to_dict_method(self):
        """Test dictionary representation"""
        review_dict = self.review.to_dict()

        self.assertEqual(review_dict["client_id"], "test_client_id")
        self.assertEqual(review_dict["restaurant_id"], "test_restaurant_id")
        self.assertEqual(review_dict["rating"], 5)
        self.assertEqual(review_dict["comment"], "Great food!")
        self.assertEqual(review_dict["__class__"], "Review")

    @patch("models.storage")
    def test_save_method(self, mock_storage):
        """Test save method"""
        old_updated_at = self.review.updated_at
        self.review.save()

        self.assertNotEqual(old_updated_at, self.review.updated_at)
        mock_storage.new.assert_called_once_with(self.review)
        mock_storage.save.assert_called_once()

    @patch("models.storage")
    def test_delete_method(self, mock_storage):
        """Test delete method"""
        self.review.delete()
        mock_storage.delete.assert_called_once_with(self.review)

    def test_attributes_types(self):
        """Test attribute types"""
        self.assertIsInstance(self.review.rating, int)
        self.assertIsInstance(self.review.comment, str)
        self.assertIsInstance(self.review.client_id, str)
        self.assertIsInstance(self.review.restaurant_id, str)


if __name__ == "__main__":
    unittest.main()
