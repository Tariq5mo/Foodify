import unittest
from console import FoodifyConsole
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel


class TestAllCommand(unittest.TestCase):

    def setUp(self):
        self.console = FoodifyConsole()

    @patch('sys.stdout', new_callable=StringIO)
    def test_all_no_class_name(self, mock_stdout):
        with patch('models.storage.all', return_value={
            'BaseModel.1234': BaseModel(id='1234'),
            'BaseModel.5678': BaseModel(id='5678')
        }):
            self.console.onecmd("all")
            output = mock_stdout.getvalue().strip()
            self.assertIn('BaseModel.1234', output)
            self.assertIn('BaseModel.5678', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_all_invalid_class_name(self, mock_stdout):
        self.console.onecmd("all InvalidClass")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class doesn't exist **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_all_valid_class_name(self, mock_stdout):
        with patch('models.storage.all', return_value={
            'BaseModel.1234': BaseModel(id='1234'),
            'User.5678': BaseModel(id='5678')
        }):
            self.console.onecmd("all BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertIn('BaseModel.1234', output)
            self.assertNotIn('User.5678', output)


if __name__ == '__main__':
    unittest.main()
