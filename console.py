#!/usr/bin/env python3
"""This module contains the console for the application."""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.review import Review
from models.order import Order

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Restaurant": Restaurant,
    "MenuItem": MenuItem,
    "Review": Review,
    "Order": Order,
}


class FoodifyConsole(cmd.Cmd):
    intro = (
        "Welcome to the Foodify console. Type 'help' or '?' to list "
        "commands.\n"
    )
    prompt = "(foodify) "

    def do_create(self, arg):
        """Create a new instance of a class."""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        new_instance = classes[args[0]]()
        # new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show string representation of an instance."""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_delete(self, arg):
        """Delete an instance."""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Print string representation of all instances."""
        if not arg:
            print([str(value) for value in storage.all().values()])
            return
        args = arg.split()
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        print(
            [
                str(value)
                for key, value in storage.all().items()
                if key.split(".")[0] == args[0]
            ]
        )

    def do_update(self, arg):
        """Update an instance."""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        instance = storage.all()[key]
        setattr(instance, args[2], args[3])
        instance.save()

    def do_search(self, arg):
        """Search for instances."""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** attribute name missing **")
            return
        if len(args) < 3:
            print("** value missing **")
            return
        print(
            [
                str(value)
                for value in storage.all().values()
                if value.__dict__[args[1]] == args[2]
            ]
        )

    def do_count(self, arg):
        """Count instances of a class."""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        print(
            len(
                [
                    value
                    for value in storage.all().values()
                    if value.__class__.__name__ == args[0]
                ]
            )
        )

    def emptyline(self):
        """Do nothing on empty input line."""
        pass

    def do_quit(self, arg):
        """Quit the console."""
        print("Goodbye!")
        return True

    def do_EOF(self, arg):
        """Handle EOF (Ctrl+D) to exit the console."""
        print("Goodbye!")
        return True

    def help_quit(self):
        print("Exits the console. Usage: quit")

    def help_EOF(self):
        print("Exits the console with EOF (Ctrl+D).")

    def help_create(self):
        print("Create a new instance of a class. Usage: create <class_name>")

    def help_show(self):
        print(
            "Show string representation of an instance. Usage: show "
            "<class_name> <id>"
        )

    def help_delete(self):
        print("Delete an instance. Usage: destroy <class_name> <id>")

    def help_all(self):
        print(
            "Print string representation of all instances. Usage: all "
            "[<class_name>]"
        )

    def help_update(self):
        print(
            "Update an instance. Usage: update <class_name> <id> "
            "<attribute> <value>"
        )

    def help_search(self):
        print(
            "Search for instances. Usage: search <class_name> <attribute> "
            "<value>"
        )

    def help_count(self):
        print(
            "Count instances of a class. Usage: count <class_name>"
        )


if __name__ == "__main__":
    FoodifyConsole().cmdloop()
