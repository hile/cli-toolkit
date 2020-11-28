
CLI scripts
===========

CLI scripts are written with :obj:`cli_toolkit.script.Script` and
:obj:`cli_toolkit.command.Command` classes. Each script consists of
one Script item and one or more Command subcommands.

Purpose of these classes is to allow defining CLI commands in declarative syntax and wrap
python's standard argparse.ArgumentParser to a class based presentation. In the end it's
all standard ArgumentParser commands.

Script object has always following arguments:

* `--debug`: if specified, script.debug() shows debug messages on stderr
* `--quiet`: if specified, script.message() output is suppressed

.. toctree::
    :maxdepth: 2
    :hidden:

    script
    command
    examples

Common attributes of script and command classes
-----------------------------------------------

 Script and Command both extend :obj:`cli_toolkit.base.NestedCliCommand`
 base class and inherit common methods:

* exit to exit CLI script with return code
* debug to send debug messages to stderr when debugging is enabled
* error to send messages to stderr regardless of debug flag, unless silenced
* message to send messages to stdout, unless silenced
