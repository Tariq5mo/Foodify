#!/usr/bin/env python3
""" Console Module """
import cmd
import sys
from models.__init__ import storage
from models.client import Client
from models.menu_item import MenuItem
from models.order_item import OrderItem
from models.order import Order
from models.restaurant import Restaurant
from models.review import Review


class FoodifyConsole(cmd.Cmd):
    """Contains the functionality for the Foodify console"""

    # determines prompt for interactive/non-interactive modes
    prompt = "(foodify) " if sys.__stdin__.isatty() else ""

    classes = {
        "Client": Client,
        "MenuItem": MenuItem,
        "OrderItem": OrderItem,
        "Order": Order,
        "Restaurant": Restaurant,
        "Review": Review,
    }
    dot_cmds = ["all", "count", "show", "destroy", "update"]
    types = {
        "price": float,
        "rating": int,
        "quantity": int,
        "latitude": float,
        "longitude": float,
        "is_available": bool
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print("(foodify)")

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ""  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ("." in line and "(" in line and ")" in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[: pline.find(".")]

            # isolate and validate <command>
            _cmd = pline[pline.find(".") + 1: pline.find("(")]
            if _cmd not in FoodifyConsole.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find("(") + 1: pline.find(")")]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(", ")  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('"', "")
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if (
                        pline[0] == "{"
                        and pline[-1] == "}"
                        and type(eval(pline)) is dict
                    ):
                        _args = pline
                    else:
                        _args = pline.replace(",", "")
                        # _args = _args.replace('\"', '')
            line = " ".join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print("(foodify) ", end="")
        return stop

    def do_quit(self, command):
        """Method to exit the foodify console"""
        exit()

    def help_quit(self):
        """Prints the help documentation for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit()

    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        pass

    def do_create(self, args):
        """Creates a new instance of a class"""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        params = {}
        for param in args[1:]:
            if "=" not in param:
                continue
            key, value = param.split("=", 1)

            # Handle string values
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            # Handle numeric values
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue

            params[key] = value

        try:
            instance = self.classes[class_name](**params)
            storage.new(instance)
            storage.save()
            print(instance.id)
        except Exception as e:
            print(f"** Error creating instance: {e} **")

    def do_show(self, args):
        """Method to show an individual object"""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        try:
            obj = storage.get(self.classes[args[0]], args[1])
            if obj:
                print(str(obj))
            else:
                print("** no instance found **")
        except Exception as e:
            print(f"** Database error: {e} **")

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Destroys a specified object"""
        if not args:
            print("** class name missing **")
            return

        args = args.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        try:
            obj = storage.get(self.classes[args[0]], args[1])
            if obj:
                obj.delete()
                storage.save()
            else:
                print("** no instance found **")
        except Exception as e:
            print(f"** Database error: {e} **")

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(" ")[0]  # remove possible trailing args
            if args not in self.classes:
                print("** class doesn't exist **")
                return

            try:
                objects = storage.all(self.classes[args])
                for obj in objects.values():
                    print_list.append(str(obj))
            except Exception as e:
                print(f"** Database error: {e} **")
                return
        else:
            try:
                objects = storage.all()
                for obj in objects.values():
                    print_list.append(str(obj))
            except Exception as e:
                print(f"** Database error: {e} **")
                return

        print(print_list)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        if not args:
            print("** class name missing **")
            return

        if args not in self.classes:
            print("** class doesn't exist **")
            return

        try:
            count = storage.count(self.classes[args])
            print(count)
        except Exception as e:
            print(f"** Database error: {e} **")

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """Updates a certain object with new info"""
        c_name = c_id = att_name = att_val = kwargs = ""

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in FoodifyConsole.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if "{" in args[2] and "}" in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = (
                []
            )  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '"':  # check for quoted arg
                second_quote = args.find('"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(" ")

            # if att_name was not quoted arg
            if not att_name and args[0] != " ":
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '"':
                att_val = args[2][1: args[2].find('"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(" ")[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if i % 2 == 0:
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in FoodifyConsole.types:
                    att_val = FoodifyConsole.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """Help information for the update class"""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    FoodifyConsole().cmdloop()