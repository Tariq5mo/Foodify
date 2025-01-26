import unittest
from console import FoodifyConsole
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel


class TestCountCommand(unittest.TestCase):

    def setUp(self):
        self.console = FoodifyConsole()

    @patch('sys.stdout', new_callable=StringIO)
    def test_count_no_class_name(self, mock_stdout):
        self.console.onecmd("count")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class name missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_count_invalid_class_name(self, mock_stdout):
        self.console.onecmd("count InvalidClass")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class doesn't exist **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_count_valid_class_name(self, mock_stdout):
        with patch('models.storage.all', return_value={
            'BaseModel.1234': BaseModel(id='1234'),
            'BaseModel.5678': BaseModel(id='5678'),
            'User.91011': BaseModel(id='91011')
        }):
            self.console.onecmd("count BaseModel")
            self.assertEqual(
                mock_stdout.getvalue().strip(), "2"
            )


if __name__ == '__main__':
    unittest.main()
