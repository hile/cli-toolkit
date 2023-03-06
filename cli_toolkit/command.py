#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI script subcommands

Subcommands can be linked to main Script instance or as nested commands to
Command instances.
"""
import argparse

from typing import Any, List, Optional, Tuple

from .base import NestedCliCommand


class Command(NestedCliCommand, argparse.ArgumentParser):
    """
    CLI subcommand

    Each CLI subcommand is initialized with parent reference. Parent must be instance
    of NestedCliCommand, i.e. Script or Command

    Arguments usage, description and epilog can be ignored and passed in child class
    as class attributes
    """

    def __init__(self,
                 parent: NestedCliCommand,
                 usage: Optional[str] = None,
                 description: Optional[str] = None,
                 epilog: Optional[str] = None) -> None:
        super().__init__(parent=parent)
        self.prog = self.name
        self.usage = self.__get_field__('usage', usage)
        self.description = self.__get_field__('description', description)
        self.epilog = self.__get_field__('epilog', epilog)

    def __get_field__(self, field: str, value: Optional[Any] = None) -> Any:
        """
        Get value for field from specified value, class attribute or using default

        If value is not not empty the command tries to use class attribute value
        """
        if value:
            return value
        return getattr(self, field)

    def exit(self, value: int = 0, message: Optional[str] = None):
        """
        Pass exit() call to parent command or script
        """
        self.__parent__.exit(value, message)

    def debug(self, *args: List[Any]) -> None:
        """
        Pass debug() call to parent command or script
        """
        self.__parent__.debug(*args)

    def error(self, *args: List[Any]) -> None:
        """
        Pass error() call to parent command or script
        """
        self.__parent__.error(*args)

    def message(self, *args: List[Any]) -> None:
        """
        Pass message() call to parent command or script
        """
        self.__parent__.message(*args)

    def parse_args(
            self,
            args: argparse.Namespace = None,
            namespace: argparse.Namespace = None) -> argparse.Namespace:
        """
        Parse command arguments

        Command arguments are received from parent and not parsed
        here with ArgumentParser default parser.
        """
        return args

    def parse_known_args(
            self,
            args: argparse.Namespace = None,
            namespace: argparse.Namespace = None) -> Tuple[argparse.Namespace, argparse.Namespace]:
        """
        Parse command arguments with unknown arguments

        Command arguments are received from parent and not parsed
        here with ArgumentParser default parser.
        """
        return args, namespace

    def run(self, args: argparse.Namespace) -> None:
        """
        Run command with arguments from argument parser
        """
        return self.run_subcommand(args)
