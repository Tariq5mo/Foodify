import unittest
from console import FoodifyConsole
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel


class TestDeleteCommand(unittest.TestCase):

    def setUp(self):
        self.console = FoodifyConsole()

    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_no_class_name(self, mock_stdout):
        self.console.onecmd("delete")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class name missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_invalid_class_name(self, mock_stdout):
        self.console.onecmd("delete InvalidClass 1234")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class doesn't exist **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_no_instance_id(self, mock_stdout):
        self.console.onecmd("delete BaseModel")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** instance id missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_non_existing_instance(self, mock_stdout):
        self.console.onecmd("delete BaseModel 1234")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** no instance found **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_existing_instance(self, mock_stdout):
        with patch('models.storage.all',
                   return_value={'BaseModel.1234': BaseModel(id='1234')}):
            self.console.onecmd("delete BaseModel 1234")
            self.assertEqual(
                mock_stdout.getvalue().strip(), ""
            )


if __name__ == '__main__':
    unittest.main()
