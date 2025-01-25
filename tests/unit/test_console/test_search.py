import unittest
from console import FoodifyConsole
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel


class TestSearchCommand(unittest.TestCase):

    def setUp(self):
        self.console = FoodifyConsole()

    @patch('sys.stdout', new_callable=StringIO)
    def test_search_no_class_name(self, mock_stdout):
        self.console.onecmd("search")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class name missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_search_invalid_class_name(self, mock_stdout):
        self.console.onecmd("search InvalidClass attr value")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class doesn't exist **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_search_no_attribute_name(self, mock_stdout):
        self.console.onecmd("search BaseModel")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** attribute name missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_search_no_value(self, mock_stdout):
        self.console.onecmd("search BaseModel attr")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** value missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_search_existing_instance(self, mock_stdout):
        with patch('models.storage.all', return_value={
            'BaseModel.1234': BaseModel(id='1234', name='test_name'),
            'BaseModel.5678': BaseModel(id='5678', name='another_name')
        }):
            self.console.onecmd("search BaseModel name test_name")
            output = mock_stdout.getvalue().strip()
            self.assertIn('BaseModel.1234', output)
            self.assertNotIn('BaseModel.5678', output)


if __name__ == '__main__':
    unittest.main()
