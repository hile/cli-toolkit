
Script class
############

Each CLI script starts with instance of :obj:`cli_toolkit.script.Script`.

Script interrupt handling
-------------------------

Script class initializes SIGINT handler. This handler calls exit() method when
script execution is cancelled.

Running script with subcommands
-------------------------------

Script is intended to be used with :obj:`cli_toolkit.command.Command` to
implement nice nested CLI commands.

Running script without subcommands
----------------------------------

Script can be run without registering subcommands and without subclassing
Script class. In this case the Script command is just a simple wrapper for
:obj:`argparse.ArgumentParser` with extra properties and you generally want
to just run parse_args() and process received arguments.
