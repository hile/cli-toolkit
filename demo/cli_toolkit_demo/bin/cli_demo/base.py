"""
Common demo base class to wrap Command to be used with multiple subcommands with shared methods and data
"""

from cli_toolkit.command import Command


class DemoCommand(Command):
    """
    Link configuration loader to demo commands
    """
    def parse_args(self, args):
        """
        Parse arguments for demo command
        """
