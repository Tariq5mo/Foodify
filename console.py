<<<<<<< HEAD
=======
#!/usr/bin/env python3
>>>>>>> 4fb386554b0b5da02ee592af690b96639016bf98
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.client import Client
from models.menu_item import MenuItem
from models.order_item import OrderItem
from models.order import Order
from models.restaurant import Restaurant
from models.review import Review


class FoodifyCommand(cmd.Cmd):
    """Contains the functionality for the Foodify console"""

    # determines prompt for interactive/non-interactive modes
    prompt = "(foodify) " if sys.__stdin__.isatty() else ""

    classes = {
        "BaseModel": BaseModel,
        "Client": Client,
        "MenuItem": MenuItem,
        "OrderItem": OrderItem,
        "Order": Order,
        "Restaurant": Restaurant,
        "Review": Review,
    }
    dot_cmds = ["all", "count", "show", "destroy", "update"]
    types = {
        "price": int,
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
            _cmd = pline[pline.find(".") + 1 : pline.find("(")]
            if _cmd not in FoodifyCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find("(") + 1 : pline.find(")")]
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

        except Exception as mess:
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
        """
        Create a new instance of any class,
        saves it DB and prints the id.

        Usage: create <class_name> attr1=value1 attr2=value2 ...
        """
        if not args:
            print("** class name missing **")
            return

        list_of_args = args.split()
        class_name = list_of_args[0]
        if class_name not in FoodifyCommand.classes:
            print("** class doesn't exist **")
            return

        dict_of_attr = {}
        for param in list_of_args[1:]:
            key_value = param.split("=")
            if len(key_value) != 2:
                continue  # Skip if parameter format is incorrect

            key, value = key_value

            # Handle value types
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                # It's a string, replace underscores with spaces and handle escaped quotes
<<<<<<< HEAD
                value = value[1:-1] #.replace('_', ' ') #.replace('"', '\\"')
            elif '.' in value:
=======
                value = value[
                    1:-1
                ]  # .replace('_', ' ') #.replace('"', '\\"')
            elif "." in value:
>>>>>>> 4fb386554b0b5da02ee592af690b96639016bf98
                try:
                    # Try converting to float
                    value = float(value)
                except ValueError:
                    continue  # Skip if converting fails
            else:
                try:
                    # Try converting to int
                    value = int(value)
                except ValueError:
                    continue  # Skip if converting fails

            dict_of_attr[key] = value

        # try:
        if class_name == Client:
            existing_client = (
                storage.session.query(Client)
                .filter_by(email=dict_of_attr["email"])
                .first()
            )
            if existing_client:
                print(f"this email is taken")
        else:
            # Create a new instance of the class
            new_instance = FoodifyCommand.classes[class_name](**dict_of_attr)
            # new_instance.save()
            storage.new(new_instance)
            storage.save()
            print(new_instance.id)
        # except KeyError:
        #     print("** email attribute missing **")
        # except Exception as e:
        #     print(f"Database error: {e}")

    def do_show(self, args):
        """Method to show an individual object"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and " " in c_id:
            c_id = c_id.partition(" ")[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in FoodifyCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Destroys a specified object"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and " " in c_id:
            c_id = c_id.partition(" ")[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in FoodifyCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del storage.all()[key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(" ")[0]  # remove possible trailing args
            if args not in FoodifyCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all(FoodifyCommand.classes[args]).items():
                if k.split(".")[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage.all(FoodifyCommand.classes[args]).items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split(".")[0]:
                count += 1
        print(count)

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
        if c_name not in FoodifyCommand.classes:  # class name invalid
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
                args = args[second_quote + 1 :]

            args = args.partition(" ")

            # if att_name was not quoted arg
            if not att_name and args[0] != " ":
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '"':
                att_val = args[2][1 : args[2].find('"', 1)]

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
                if att_name in FoodifyCommand.types:
                    att_val = FoodifyCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """Help information for the update class"""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    FoodifyCommand().cmdloop()
