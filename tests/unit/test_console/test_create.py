import unittest
from console import FoodifyConsole
from unittest.mock import patch
from io import StringIO


class TestCreateCommand(unittest.TestCase):

    def setUp(self):
        self.console = FoodifyConsole()

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_no_class_name(self, mock_stdout):
        self.console.onecmd("create")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class name missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_invalid_class_name(self, mock_stdout):
        self.console.onecmd("create InvalidClass")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class doesn't exist **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_valid_class_name(self, mock_stdout):
        with patch('models.base_model.BaseModel.save()'):
            self.console.onecmd("create BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertTrue(len(output) > 0)  # Check if an ID was printed


if __name__ == '__main__':
    unittest.main()
