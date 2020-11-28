# CLI toolkit for shell command utilities

This module contains modules to implement CLI scripts by wrapping
python argparse.ArgumentParser to user friendly utility classes.

## Create a script class

Main class to use is the Script class. It will get it's name from
sys.argv[0].

Example:

```python
from cli_toolkit.script import Script

if __name__ == '__main__':
    script = Script()
    script.add_argument('files', nargs='*', help='Files to process')
    args = script.parse_args()
    for filename in args.files:
        script.debug('PROCESSING', filename)
        script.message(filename)
```

Running the example:

```
> python test.py foo bar
foo
bar
```

This is pretty straightforward ArgumentParser, except it

* sets SIGINT handler
* adds --debug and --quiet flags
* adds `debug` and `message` functions which honor the debug and quiet flags

## Using script with subcommands

More useful is using a script with subcommands. The subcommands require
at least `name` class variable and should have `usage`, `description` and
`epilog`.

You also should implement `run` method and call script.run() to run correct
subcommand. Arguments for subcommand parser are registered with method
`register_parser_arguments`.

```python
from cli_toolkit.script import Script
from cli_toolkit.command import Command


class ListCommand(Command):
    name = 'list'
    usage = 'List files'
    description = 'Lists files specified on command line'

    def register_parser_arguments(self, parser):
        parser.add_argument('files', nargs='*', help='Files to process')

    def run(self, args):
        for filename in args.files:
            self.debug('PROCESSING', filename)
            self.message(filename)


if __name__ == '__main__':
    script = Script()
    script.add_subcommand(ListCommand(script))
    script.run()
```

Running the example:

```bash
> python test.py list foo bar
foo
bar
```

## Using nested subcommands

The subcommands can be nested. You need to pass the parser in paren't
register_parser_subcommand to add_subcommand.

```python
from cli_toolkit.script import Script
from cli_toolkit.command import Command


class FilesCommand(Command):
    name = 'demo'
    usage = 'Run nested demo subcommands'

    def register_parser_arguments(self, parser):
        """
        Register 'list' command under demo subcommand
        """
        self.add_subcommand(ListCommand(self), parser)
        return parser


class ListCommand(Command):
    name = 'list'
    usage = 'List files'
    description = 'Lists files specified on command line'

    def register_parser_arguments(self, parser):
        """
        Register 'list' command arguments
        """
        parser.add_argument('files', nargs='*', help='Files to process')
        return parser

    def run(self, args):
        if not args.files:
            self.exit(1, 'No files provided')
        for filename in args.files:
            self.debug('PROCESSING', filename)
            self.message(filename)


if __name__ == '__main__':
    script = Script()
    script.add_subcommand(FilesCommand(script))
    script.run()
```

Running the example:

```bash
> python test.py demo list foo bar
foo
bar
```
