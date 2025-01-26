#!/usr/bin/python3
"""Unit tests for console.py"""
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from console import FoodifyConsole
from models.client import Client
from models.restaurant import Restaurant


class TestFoodifyConsole(unittest.TestCase):
    """Test cases for FoodifyConsole class"""

    def setUp(self):
        """Set up test cases"""
        self.console = FoodifyConsole()
        self.mock_stdout = StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        """Clean up after tests"""
        sys.stdout = sys.__stdout__
        self.mock_stdout.close()

    def _last_write(self, nr=None):
        """Returns last n output lines"""
        if nr is None:
            return self.mock_stdout.getvalue()
        return self.mock_stdout.getvalue().split("\n")[nr]

    @patch("console.storage")
    @patch("models.storage")
    def test_do_create_client(
        self, mock_models_storage, mock_console_storage
    ):
        """Test create command with Client class"""
        mock_instance = Client()
        mock_instance.id = "test_id"
        mock_console_storage.new = MagicMock()
        mock_console_storage.save = MagicMock()

        # Patch 'console.Client' instead of 'models.client.Client'
        with patch("console.Client") as mock_client:
            mock_client.return_value = mock_instance
            self.console.do_create(
                'Client id="test_id" name="Test User" email="test@test.com" password="test123" address="Test St"'
            )

        mock_console_storage.new.assert_called_once()
        mock_console_storage.save.assert_called_once()
        self.assertEqual(self._last_write(0), "test_id")

    @patch("console.storage")
    def test_do_show(self, mock_storage):
        """Test show command"""
        test_instance = Client()
        test_instance.id = "test_id"
        mock_storage.get.return_value = test_instance

        self.console.do_show("Client test_id")
        mock_storage.get.assert_called_with(Client, "test_id")

    @patch("console.storage")
    def test_do_all(self, mock_storage):
        """Test all command"""
        test_instances = {"Client.1": Client(), "Restaurant.1": Restaurant()}
        mock_storage.all.return_value = test_instances

        self.console.do_all("")
        mock_storage.all.assert_called_once()

    @patch("console.storage")
    def test_do_destroy(self, mock_storage):
        """Test destroy command"""
        test_instance = Client()
        mock_storage.get.return_value = test_instance

        self.console.do_destroy("Client test_id")
        mock_storage.get.assert_called_with(Client, "test_id")
        mock_storage.save.assert_called_once()

    def test_do_quit(self):
        """Test quit command"""
        with self.assertRaises(SystemExit):
            self.console.do_quit("")

    @patch("console.storage")
    @patch("models.storage")
    def test_do_update(self, mock_models_storage, mock_console_storage):
        """Test update command"""
        # Provide required fields for Client to avoid IntegrityError
        test_instance = Client(
            id="test_id",
            username="TestUser",
            address="TestAddress",
            email="old@test.com",
            password="oldpass",
        )
        mock_console_storage.all.return_value = {
            "Client.test_id": test_instance
        }

        self.console.do_update("Client test_id email new@test.com")
        self.assertEqual(test_instance.email, "new@test.com")

    def test_invalid_class(self):
        """Test commands with invalid class name"""
        self.console.do_create("InvalidClass")
        self.assertIn("** class doesn't exist **", self._last_write())

    def test_missing_class(self):
        """Test commands with missing class name"""
        self.console.do_create("")
        self.assertIn("** class name missing **", self._last_write())

    @patch("console.storage")
    def test_do_count(self, mock_storage):
        """Test count command"""
        mock_storage.count.return_value = 5

        self.console.do_count("Client")
        mock_storage.count.assert_called_with(Client)
        self.assertEqual(self._last_write(0), "5")


if __name__ == "__main__":
    unittest.main()