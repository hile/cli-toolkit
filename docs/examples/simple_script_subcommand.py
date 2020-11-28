#!/usr/bin/env python3

from cli_toolkit.script import Script
from cli_toolkit.command import Command


class DemoCommand(Command):
    """
    Trivial demo command to show passed tag
    """
    name = 'demo'
    usage = 'demo <args>'

    @staticmethod
    def register_parser_arguments(parser):
        parser.add_argument('-t', '--tag', help='Demo tag')

    def run(self, args):
        if args.tag:
            # Shows message on sys.stdout unless --quiet is specified
            self.message(args.tag)
        else:
            # Sends message to sys.stderr
            self.error('No tag specified')


# Linking subcommands automatically by specifying in custom child class
class DemoScript(Script):
    """
    Demo script with single subcommand
    """
    subcommands = (
        DemoCommand
    )


if __name__ == '__main__':
    DemoScript().run()


# Linking subcommands manually with add_subcommand method and raw Script class
if __name__ == '__main__':
    script = Script()
    script.add_subcommand(DemoCommand(script))
    script.run()
