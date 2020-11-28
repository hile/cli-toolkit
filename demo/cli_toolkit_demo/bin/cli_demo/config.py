"""
CLI command 'cli-demo config' to show contents of demo app configuration
"""

from .base import DemoCommand


class Config(DemoCommand):
    """
    Show cli-demo configuration
    """
    name = 'config'
    """Defines name for subcommand used on command line"""

    def run(self, args):
        """
        Run the subcommand

        run() method is always required unless subcommand is a parser for nested subcommands
        """
        print('show configuration')
