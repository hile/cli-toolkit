#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
CLI script base class

This module implements the common base class to quickly create CLI commands
with python.

The Script class is usually used with cli_toolkit.command.Command to create
CLI scripts with subcommands.
"""
import argparse
import signal
import sys

from pathlib import Path
from types import FrameType
from typing import Any, Dict, List, Optional, Tuple

from sys_toolkit.logger import Logger

from .base import NestedCliCommand


class ScriptMetaClass(type):
    """
    Run script initialize() method after creating object
    """
    def __call__(cls, *args: List[Any], **kwargs: Dict[Any, Any]) -> None:
        obj = type.__call__(cls, *args, **kwargs)
        obj.initialize()
        return obj


class Script(NestedCliCommand, metaclass=ScriptMetaClass):
    """
    CLI script command main class
    """
    name: str
    logger: Logger
    __parser__: argparse.ArgumentParser

    subcommands: Tuple[NestedCliCommand] = ()

    def __init__(self,
                 usage: str = None,
                 description: str = None,
                 epilog: str = None,
                 formatter_class: argparse.HelpFormatter = None) -> None:
        signal.signal(signal.SIGINT, self.SIGINT)
        self.name = Path(sys.argv[0]).name
        self.logger = Logger(self.name)
        super().__init__()

        if formatter_class is None:
            formatter_class = self.default_formatter_class

        self.__parser__ = argparse.ArgumentParser(
            prog=self.name,
            usage=usage if usage is not None else self.usage,
            description=description if description is not None else self.description,
            epilog=epilog if epilog is not None else self.epilog,
            formatter_class=formatter_class,
            add_help=True,
            conflict_handler='resolve',
        )

        self.__parser__.add_argument('--debug', action='store_true', help='Enable debug messages')
        self.__parser__.add_argument('--quiet', action='store_true', help='Silent printed messages')

    # pylint: disable=unused-argument
    def initialize(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> None:
        """
        Add subcommands defined in self.subcommands after creating object instance
        """
        self.register_parser_arguments(self.__parser__)
        self.__register_subcommands__()

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    def SIGINT(self, signum: int, frame: Optional[FrameType]) -> None:
        """
        Parse SIGINT signal by quitting the program cleanly with exit code 1
        """
        self.reset_stty()
        self.exit(1)

    def __process_args__(self, args: argparse.Namespace) -> argparse.Namespace:
        """
        Process args and run subcommand if detected
        """
        if getattr(args, 'debug', None):
            self.__debug_enabled__ = True

        if getattr(args, 'quiet', None):
            self.__silent__ = True

        return args

    def parse_args(self) -> argparse.Namespace:
        """
        Call parse_args for parser and check for default logging flags
        """
        return self.__process_args__(self.__parser__.parse_args())

    def parse_known_args(self) -> Tuple[argparse.Namespace, argparse.Namespace]:
        """
        Call parse_args for parser and check for default logging flags
        """
        args, other_args = self.__parser__.parse_known_args()
        args = self.__process_args__(args)
        return args, other_args

    def run(self) -> None:
        """
        Run script, parsing arguments and running subcommands

        This expects subcommands have been registered and exists if not

        This simply runs self.parse_args() not expecting to do anything with
        returned values since the subcommand is run.
        """
        args = self.parse_args()
        self.run_subcommand(args)
