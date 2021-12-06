"""
CLI script subcommands

Subcommands can be linked to main Script instance or as nested commands to
Command instances.
"""

import argparse

from .base import NestedCliCommand


class Command(NestedCliCommand, argparse.ArgumentParser):
    """
    CLI subcommand

    Each CLI subcommand is initialized with parent reference. Parent must be instance
    of NestedCliCommand, i.e. Script or Command

    Arguments usage, description and epilog can be ignored and passed in child class
    as class attributes
    """

    def __init__(self, parent, usage=None, description=None, epilog=None):
        super().__init__(parent=parent)
        self.prog = self.name
        self.usage = self.__get_field__('usage', usage)
        self.description = self.__get_field__('description', description)
        self.epilog = self.__get_field__('epilog', epilog)

    def __get_field__(self, field, value=None):
        """
        Get value for field from specified value, class attribute or using default

        If value is not not empty the command tries to use class attribute value
        """
        if value:
            return value
        return getattr(self, field)

    def exit(self, value=0, message=None):
        """
        Pass exit() call to parent command or script
        """
        self.__parent__.exit(value, message)

    def debug(self, *args):
        """
        Pass debug() call to parent command or script
        """
        self.__parent__.debug(*args)

    def error(self, *args):
        """
        Pass error() call to parent command or script
        """
        self.__parent__.error(*args)

    def message(self, *args):
        """
        Pass message() call to parent command or script
        """
        self.__parent__.message(*args)

    def parse_args(self, args=None, namespace=None):
        """
        Parse command arguments

        Command arguments are received from parent and not parsed
        here with ArgumentParser default parser.
        """
        return args

    def parse_known_args(self, args=None, namespace=None):
        """
        Parse command arguments with unknown arguments

        Command arguments are received from parent and not parsed
        here with ArgumentParser default parser.
        """
        return args, namespace

    def run(self, args):
        """
        Run command with arguments from argument parser
        """
        return self.run_subcommand(args)
