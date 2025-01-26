#!/usr/bin/python3
"""Unit tests for BaseModel class"""
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test cases"""
        self.model = BaseModel()

    def test_init_without_args(self):
        """Test initialization without arguments"""
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_init_with_kwargs(self):
        """Test initialization with keyword arguments"""
        test_id = "test-id-123"
        test_date = datetime.now()
        model = BaseModel(
            id=test_id,
            created_at=test_date.isoformat(),
            updated_at=test_date.isoformat(),
        )
        self.assertEqual(model.id, test_id)

    def test_str_representation(self):
        """Test string representation of the model"""
        self.model.id = "test-id-123"
        expected = "[BaseModel] (test-id-123)"
        self.assertTrue(str(self.model).startswith(expected))

    @patch("models.storage")
    def test_save_method(self, mock_storage):
        """Test save method"""
        old_updated_at = self.model.updated_at
        mock_storage.save = MagicMock()

        self.model.save()

        self.assertNotEqual(old_updated_at, self.model.updated_at)
        mock_storage.new.assert_called_once_with(self.model)
        mock_storage.save.assert_called_once()

    def test_to_dict_method(self):
        """Test dictionary representation of the model"""
        test_dict = self.model.to_dict()

        self.assertIsInstance(test_dict, dict)
        self.assertEqual(test_dict["__class__"], "BaseModel")
        self.assertIsInstance(test_dict["created_at"], str)
        self.assertIsInstance(test_dict["updated_at"], str)
        self.assertNotIn("_sa_instance_state", test_dict)

    def test_to_dict_with_custom_attributes(self):
        """Test to_dict with additional attributes"""
        self.model.custom_attr = "test_value"
        test_dict = self.model.to_dict()

        self.assertIn("custom_attr", test_dict)
        self.assertEqual(test_dict["custom_attr"], "test_value")

    @patch("models.storage")
    def test_delete_method(self, mock_storage):
        """Test delete method"""
        mock_storage.delete = MagicMock()

        self.model.delete()

        mock_storage.delete.assert_called_once_with(self.model)

    def test_init_ignores_class_attr(self):
        """Test that __class__ attribute is ignored in kwargs"""
        model = BaseModel(__class__="SomeOtherClass")
        self.assertEqual(model.__class__.__name__, "BaseModel")

    def test_updated_at_changes_on_save(self):
        """Test that updated_at changes when save is called"""
        original_updated_at = self.model.updated_at
        with patch("models.storage"):
            self.model.save()
        self.assertNotEqual(original_updated_at, self.model.updated_at)


if __name__ == "__main__":
    unittest.main()
