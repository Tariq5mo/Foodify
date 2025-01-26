import unittest
from console import FoodifyConsole
from models import storage
from models.base_model import BaseModel
from io import StringIO
import sys


class TestShowCommand(unittest.TestCase):
    def setUp(self):
        self.console = FoodifyConsole()
        self.stdout = StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__
        storage.all().clear()

    def test_show_missing_class_name(self):
        self.console.onecmd("show")
        self.assertEqual(self.stdout.getvalue().strip(),
                         "** class name missing **")

    def test_show_class_does_not_exist(self):
        self.console.onecmd("show NonExistentClass 1234")
        self.assertEqual(self.stdout.getvalue().strip(),
                         "** class doesn't exist **")

    def test_show_missing_instance_id(self):
        self.console.onecmd("show BaseModel")
        self.assertEqual(self.stdout.getvalue().strip(),
                         "** instance id missing **")

    def test_show_instance_not_found(self):
        self.console.onecmd("show BaseModel 1234")
        self.assertEqual(self.stdout.getvalue().strip(),
                         "** no instance found **")

    def test_show_instance(self):
        instance = BaseModel()
        storage.new(instance)
        self.console.onecmd(f"show BaseModel {instance.id}")
        self.assertIn(instance.id, self.stdout.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
