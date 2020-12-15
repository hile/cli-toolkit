"""
Base classes for scripts and script subcommands
"""

import argparse
import asyncio
import os
import sys

from .exceptions import ScriptError
from .logger import Logger, DEFAULT_TARGET_NAME

DEFAULT_SUBPARSER_HELP = ''


class Meta(type):
    """
    Metaclass to run initialize() method after init
    """
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.initialize(*args, **kwargs)
        return instance


class Base(metaclass=Meta):
    """
    Base class with message / error handling and runner for registered
    async tasks

    Also includes self.logger instance of cli_toolkit.logger.Logger with
    specified logger group name
    """
    def __init__(self, parent=None, debug_enabled=False, silent=False, logger=DEFAULT_TARGET_NAME):
        if parent is not None and not isinstance(parent, Base):
            raise TypeError('parent must be instance of cli_toolkit.base.Base')
        self.__parent__ = parent
        self.__logger__ = Logger(logger)

        self.__debug_enabled__ = debug_enabled
        self.__silent__ = silent

        self.__async_task_callbacks__ = []
        self.__async_tasks__ = []

    @property
    def __is_debug_enabled__(self):
        """
        Check if debugging is enabled in this class or parents
        """
        if self.__parent__ is not None:
            return self.__parent__.__is_debug_enabled__ or self.__debug_enabled__
        return self.__debug_enabled__

    @property
    def __is_silent__(self):
        """
        Check if silent mode is enabled in this class or parents
        """
        if self.__parent__ is not None:
            return self.__parent__.__is_silent__ or self.__silent__
        return self.__silent__

    @staticmethod
    def __parse_string_args__(*args):
        """
        Parse list of values as stripped string concatenated by space
        """
        args = [str(arg).rstrip() for arg in args]
        return ' '.join(args)

    def debug(self, *args):
        """
        Send debug message to stderr if debug mode is enabled
        """
        if self.__is_debug_enabled__:
            self.error(*args)

    def error(self, *args):
        """
        Send error message to stderr
        """
        sys.stderr.write(f'{self.__parse_string_args__(*args)}\n')

    def message(self, *args):
        """
        Show message to stdout unless silent flag is set
        """
        if not self.__is_silent__:
            sys.stdout.write(f'{self.__parse_string_args__(*args)}\n')

    def add_async_task_callback(self, callback, **kwargs):
        """
        Add async task to be run
        """
        self.__async_task_callbacks__.append((callback, kwargs))

    async def run_async_tasks(self):
        """
        Run asynchronous tasks added by self.add_task
        """
        self.__async_tasks__ = []

        for callback_args in self.__async_task_callbacks__:
            callback = callback_args[0]
            kwargs = callback_args[1]
            task = asyncio.create_task(callback(**kwargs))
            self.__async_tasks__.append(task)

        for task in self.__async_tasks__:
            await task

        return asyncio.gather(*self.__async_tasks__)

    # pylint: disable=unused-argument
    def initialize(self, *args, **kwargs):
        """
        Method run after initializing object

        Implement in child class if needed
        """


class NestedCliCommand(Base):
    """
    Common base class for scripts and nested CLI commands
    """
    name = None
    """Name of script or command, used in CLI command arguments generation"""
    usage = ''
    """Command usage string for --help in ArgumentParser"""
    description = ''
    """Command description, shown on top of --help output"""
    epilog = ''
    """Command epilog, shown on botton of --help output"""
    default_formatter_class = argparse.RawTextHelpFormatter
    """Argument parser formatter class"""
    no_subcommand_error = 'No command selected'
    """Error message to show when no required subcommand is specified when running CLI"""

    subcommands = ()

    def __init__(self, parent=None):
        """
        Initialize command with link t parent

        Parent can be either Script or Command
        """

        if parent is not None and not isinstance(parent, NestedCliCommand):
            raise TypeError('parent must be instance of NestedCliCommand')

        super().__init__(parent=parent)
        self.__subcommand_parser__ = None
        self.__subcommands__ = {}

        self.__parser__ = parent.__parser__ if parent is not None else None

        if self.name is None:
            raise ScriptError(f'No name defined: {self.__class__}')

    def __repr__(self):
        """
        Return name of script or command
        """
        return self.name if self.name is not None else ''

    @property
    def command_dest(self):
        """
        Return ArgumentParser 'dest' flag for command
        """
        return f'{self.name}_command'

    def exit(self, value=0, message=None):
        """
        Exit the script with given exit value

        If message is not None, it is output to stderr
        """
        if isinstance(value, bool):
            value = 0 if value else 1
        else:
            try:
                value = int(value)
                if value < 0 or value > 255:
                    raise ValueError
            except ValueError:
                value = 1

        if message:
            self.error(message)

        for task in self.__async_tasks__:
            task.cancel()

        self.reset_stty()
        sys.exit(value)

    def __register_subcommands__(self):
        """
        Register nested subcommands
        """
        for loader in self.subcommands:
            command = loader(self)
            if command.name not in self.__subcommands__:
                self.add_subcommand(command)
            command.__register_subcommands__()

    @staticmethod
    def reset_stty():
        """
        Clear stty settings by running 'stty sane' in terminal
        """
        try:
            os.system('stty sane')
        except Exception:
            pass

    # pylint: disable=redefined-builtin
    def add_subparsers(self, help=None):
        """
        Add subparsers linked to parent parser
        """
        assert self.__parser__ is not None
        assert self.__subcommand_parser__ is None

        if help is None:
            help = DEFAULT_SUBPARSER_HELP

        self.__subcommand_parser__ = self.__parser__.add_subparsers(
            dest=self.command_dest,
            help=help,
        )
        self.__subcommands__ = {}

    # pylint: disable=redefined-builtin
    def add_subcommand(self, command, help=None, formatter_class=None):
        """
        Add a subcommand parser linked to nested command
        """
        if self.__subcommand_parser__ is None:
            self.add_subparsers(help=help)

        if formatter_class is None:
            formatter_class = self.default_formatter_class

        if command.name in self.__subcommands__:
            self.exit(1, f'Subcommand already registered: {self} {command.name}')

        parser = self.__subcommand_parser__.add_parser(
            name=command.name,
            usage=getattr(command, 'usage', None),
            description=getattr(command, 'description', None),
            epilog=getattr(command, 'epilog', None),
            formatter_class=formatter_class,
        )
        command.__parser__ = parser
        self.__subcommands__[command.name] = command

        parser = command.register_parser_arguments(parser)

        command.__register_subcommands__()
        return parser

    def add_argument(self, *args, **kwargs):
        """
        Shortcut to add argument to main argumentparser instance
        """
        self.__parser__.add_argument(*args, **kwargs)

    @staticmethod
    def register_parser_arguments(parser):
        """
        Register parser arguments

        By default does nothing
        """
        return parser

    def run_subcommand(self, args):
        """
        Run subcommand with arguments
        """
        if self.__async_task_callbacks__:
            asyncio.run(self.run_async_tasks())
            self.exit(0)

        if self.command_dest not in args:
            self.exit(1, 'Command defines no subcommands')

        command_dest = getattr(args, self.command_dest, None)
        if command_dest is None:
            self.exit(1, self.no_subcommand_error)

        command = self.__subcommands__[command_dest]
        args = command.parse_args(args)
        command.run(args)
        # Explicitly exit after running command
        self.exit(0)
