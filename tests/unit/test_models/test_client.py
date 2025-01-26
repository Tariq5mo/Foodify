#!/usr/bin/python3
"""Unit tests for Client class"""
import unittest
from unittest.mock import patch
from models.client import Client


class TestClient(unittest.TestCase):
    """Test cases for Client model"""

    def setUp(self):
        """Set up test cases"""
        self.client = Client(
            username="testuser",
            email="test@example.com",
            password="test123",
            address="123 Test St",
        )

    def test_init_required_attributes(self):
        """Test initialization with required attributes"""
        self.assertEqual(self.client.username, "testuser")
        self.assertEqual(self.client.email, "test@example.com")
        self.assertEqual(self.client.password, "test123")
        self.assertEqual(self.client.address, "123 Test St")

    def test_init_optional_attributes(self):
        """Test initialization with optional attributes"""
        client = Client(
            username="testuser",
            email="test@example.com",
            password="test123",
            address="123 Test St",
            phone="1234567890",
            latitude=40.7128,
            longitude=-74.0060,
            delivery_instructions="Leave at door",
        )
        self.assertEqual(client.phone, "1234567890")
        self.assertEqual(client.latitude, 40.7128)
        self.assertEqual(client.longitude, -74.0060)
        self.assertEqual(client.delivery_instructions, "Leave at door")

    def test_str_representation(self):
        """Test string representation"""
        self.client.id = "test123"
        string = str(self.client)
        self.assertIn("[Client] (test123)", string)
        self.assertIn("testuser", string)
        self.assertIn("test@example.com", string)

    def test_to_dict_method(self):
        """Test dictionary representation"""
        client_dict = self.client.to_dict()
        self.assertEqual(client_dict["username"], "testuser")
        self.assertEqual(client_dict["email"], "test@example.com")
        self.assertEqual(client_dict["address"], "123 Test St")
        self.assertEqual(client_dict["__class__"], "Client")

    @patch("models.storage")
    def test_save_method(self, mock_storage):
        """Test save method"""
        old_updated_at = self.client.updated_at
        self.client.save()
        self.assertNotEqual(old_updated_at, self.client.updated_at)
        mock_storage.new.assert_called_once_with(self.client)
        mock_storage.save.assert_called_once()

    @patch("models.storage")
    def test_delete_method(self, mock_storage):
        """Test delete method"""
        self.client.delete()
        mock_storage.delete.assert_called_once_with(self.client)

    def test_update_method(self):
        """Test update method with allowed fields"""
        new_email = "newemail@example.com"
        new_address = "456 New St"

        self.client.update(email=new_email, address=new_address)

        self.assertEqual(self.client.email, new_email)
        self.assertEqual(self.client.address, new_address)

    def test_update_method_invalid_field(self):
        """Test update method with invalid field"""
        original_username = self.client.username
        self.client.update(username="newusername")  # Should not update
        self.assertEqual(self.client.username, original_username)

    def test_user_mixin_methods(self):
        """Test UserMixin required methods"""
        self.assertTrue(hasattr(self.client, "is_authenticated"))
        self.assertTrue(hasattr(self.client, "is_active"))
        self.assertTrue(hasattr(self.client, "is_anonymous"))
        self.assertTrue(hasattr(self.client, "get_id"))


if __name__ == "__main__":
    unittest.main()
... (1 line left)
