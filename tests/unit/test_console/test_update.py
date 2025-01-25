import unittest
from console import FoodifyConsole
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel


class TestUpdateCommand(unittest.TestCase):

    def setUp(self):
        self.console = FoodifyConsole()

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_no_class_name(self, mock_stdout):
        self.console.onecmd("update")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class name missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_invalid_class_name(self, mock_stdout):
        self.console.onecmd("update InvalidClass 1234 attr value")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** class doesn't exist **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_no_instance_id(self, mock_stdout):
        self.console.onecmd("update BaseModel")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** instance id missing **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_non_existing_instance(self, mock_stdout):
        self.console.onecmd("update BaseModel 1234 attr value")
        self.assertEqual(
            mock_stdout.getvalue().strip(), "** no instance found **"
        )

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_no_attribute_name(self, mock_stdout):
        with patch('models.storage.all',
                   return_value={'BaseModel.1234': BaseModel(id='1234')}):
            self.console.onecmd("update BaseModel 1234")
            self.assertEqual(
                mock_stdout.getvalue().strip(), "** attribute name missing **"
            )

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_no_value(self, mock_stdout):
        with patch('models.storage.all',
                   return_value={'BaseModel.1234': BaseModel(id='1234')}):
            self.console.onecmd("update BaseModel 1234 attr")
            self.assertEqual(
                mock_stdout.getvalue().strip(), "** value missing **"
            )

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_existing_instance(self, mock_stdout):
        with patch('models.storage.all',
                   return_value={'BaseModel.1234': BaseModel(id='1234')}):
            self.console.onecmd("update BaseModel 1234 name test_name")
            instance = storage.all()['BaseModel.1234']
            self.assertEqual(instance.name, 'test_name')


if __name__ == '__main__':
    unittest.main()
