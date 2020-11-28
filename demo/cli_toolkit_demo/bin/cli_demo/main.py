"""
CLI command demo application 'cli-demo'
"""

from cli_toolkit.script import Script

from .config import Config


class CLIDemo(Script):
    """
    Main script entrypoint for cli-demo command
    """
    subcommands = (
        Config,
    )
    """Classes for subcommands to load. Linked automatically to script"""


def main():
    """
    Main entrypoint for cli-demo command, linked to setup.py
    """
    CLIDemo().run()
