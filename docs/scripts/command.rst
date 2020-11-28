
Command class
#############

CLI scripts subcommands are implemented with :obj:`cli_toolkit.command.Command`
classes.

This class is only intended to be used as parent class for custom classes.


Minimal subclass attributes
----------------------------------

Each custom Command subclass must implement at least following:

* have `name` class attribute

    Name is used to link command to it's parent and must be unique in parent scope

* implement `run(self, args)` method

    Run method is called to execute the command. Args contains arguments received
    from argument parser for the command

Optional subclass attributes
-----------------------------------

Following attributess of custom subclasses are not required but highly recommented.

* `usage` class attribute

    Usage is used with --help information to show usage example for the command

* `description` class attribute

    Description is shown at top of --help output to describe the command. This should be a
    multiline string.

* `epilog` class attribute

    Epilog is shown at bottom of --help to further describe the command. This should be a
    multiline string.

* register_parser_arguments(self, parser) method

    This method is used to register command line arguments for the command.

    This method must return received parser.

* parse_args(self, args) method

    This method is used to parse command arguments before running the command. Args
    is the list of arguments received from ArgumentParser.

    This method must return received args.

Binding commands to script
--------------------------

Command instances are useless standalone. Each instance must be linked as subcommand
to either Script or Command instances with `add_subcommand(parent)` method, where
parent is the parent Script or Command instance.

Linking commands to a Script instance:

.. code-block:: python

    from cli_toolkit.script import Script
    from commands.mycommand import MyCommand

    script = Script()
    script.add_subcommand(MyCommand(script))
    script.run()


Binding subcommands to command
------------------------------

Commands can be nested under each other to created nested parsers:

.. code-block:: bash

    example-script my-command subcommand --help

Linking commands to a Command instance is done in `register_parser_arguments` method
of custom Command class, passing the global parser as extra argument:

.. code-block:: python

    from cli_toolkit.command import Command
    from .subcommands import SubCommand

    class MyCommand(Command):
        name = 'my-command'

        def register_parser_arguments(self, parser):
            self.add_subcommand(SubCommand(self), parser)
            return parse_args

        def run(self, args):
            self.message('args', args)
