#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for subcommands in cli_toolkit.command module
"""
import argparse
import sys

import pytest

from cli_toolkit.base import ScriptError, DEFAULT_SUBPARSER_HELP
from cli_toolkit.script import Script
from cli_toolkit.command import Command


class EmptyCommand(Command):
    """
    Empty command without run method
    """
    name = 'empty'


class ResultsCommand(Command):
    """
    Command where running sets result to True
    """
    name = 'empty'
    usage = 'Test empty with result'
    result = False

    def run(self, args: argparse.Namespace):
        self.result = True


class SubcommandsScript(Script):
    """
    Script with subcommands loaded from subcommands attribute
    """
    subcommands = (
        EmptyCommand,
    )


# pylint: disable=redefined-builtin
def initialize_empty_command(help_message=None, formatter_class=None) -> None:
    """
    Initialize empty command with script for tests
    """
    script = Script()
    command = EmptyCommand(script)
    script.add_subcommand(command, help=help_message, formatter_class=formatter_class)

    if formatter_class is None:
        formatter_class = command.default_formatter_class
    # pylint: disable=protected-access
    parser_args = script.__subcommand_parser__._name_parser_map[command.name]
    assert parser_args.formatter_class == formatter_class
    return script, command


def test_create_subcommands_script() -> None:
    """
    Test creating script with subcommands from class attribute
    """
    script = SubcommandsScript()
    name = 'empty'
    assert name in script.__subcommands__
    command = script.__subcommands__[name]
    assert isinstance(command, EmptyCommand)
    assert script.__subcommands__[name].__hash__() == command.__hash__()

    script.__register_subcommands__()
    assert script.__subcommands__[name].__hash__() == command.__hash__()


def test_create_subcommand_no_name() -> None:
    """
    Test adding command without name
    """
    script = Script()
    with pytest.raises(ScriptError):
        script.add_subcommand(Command(script))


def test_create_empty_command() -> None:
    """
    Test creating script with empty command
    """
    script, command = initialize_empty_command()
    with pytest.raises(SystemExit) as exit_code:
        script.run()
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1
    assert command.usage == ''
    assert script.__subcommand_parser__.help == DEFAULT_SUBPARSER_HELP


def test_create_empty_command_with_help() -> None:
    """
    Test creating script with empty command
    """
    help_message = 'Helpful message'
    script, command = initialize_empty_command(help_message=help_message)
    with pytest.raises(SystemExit) as exit_code:
        script.run()
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1
    assert command.usage == ''
    assert script.__subcommand_parser__.help == help_message


def test_create_empty_command_with_formatter_class() -> None:
    """
    Test creating script with empty command and custom formatter class
    """
    help_message = 'Helpful message'
    formatter_class = argparse.RawDescriptionHelpFormatter
    script, command = initialize_empty_command(
        help_message=help_message,
        formatter_class=formatter_class
    )
    with pytest.raises(SystemExit) as exit_code:
        script.run()
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1
    assert command.usage == ''
    assert script.__subcommand_parser__.help == help_message


def test_command_with_other_args() -> None:
    """
    Test parsing script with other args
    """
    script, command = initialize_empty_command()
    args, other_args = script.parse_known_args()
    command.parse_known_args(args, other_args)


def test_create_command_custom_fields() -> None:
    """
    Test adding command without name
    """
    script = Script()
    usage = 'Test usage'
    description = 'Test description'
    epilog = 'Test epilog'
    command = EmptyCommand(
        script,
        usage=usage,
        description=description,
        epilog=epilog
    )
    script.add_subcommand(command)
    assert usage == command.usage
    assert description == command.description
    assert epilog == command.epilog


def test_reregister_command() -> None:
    """
    Test registrering same command twice
    """
    script, _command = initialize_empty_command()
    with pytest.raises(SystemExit) as exit_code:
        script.add_subcommand(EmptyCommand(script))
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1


def test_debug_flag_default() -> None:
    """
    Test script subcommand has debugging disabled by default
    """
    script, _command = initialize_empty_command()
    assert script.__is_debug_enabled__ is False
    for command in script.__subcommands__.values():
        assert command.__is_debug_enabled__ is False


def test_debug_flag_inheritance() -> None:
    """
    Test script subcommand debug flag follows script
    """
    script, _command = initialize_empty_command()
    script.__debug_enabled__ = True
    assert script.__is_debug_enabled__ is True
    for command in script.__subcommands__.values():
        assert command.__is_debug_enabled__ is True


def test_debug_message_debug(capsys) -> None:
    """
    Test sending debug message with debug disabled
    """
    script, command = initialize_empty_command()
    assert script.__is_debug_enabled__ is False
    assert script.__is_silent__ is False
    message = 'Test silent debug message'
    command.debug(message)
    captured = capsys.readouterr()
    assert captured.err == ''


def test_debug_message_enabled(capsys) -> None:
    """
    Test sending debug message with debug disabled
    """
    script, command = initialize_empty_command()
    script.__debug_enabled__ = True
    message = 'Test silent debug message'
    command.debug(message)
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_silent_flag_default() -> None:
    """
    Test script subcommand has silent disabled by default
    """
    script, _command = initialize_empty_command()
    assert script.__is_silent__ is False
    for command in script.__subcommands__.values():
        assert command.__is_silent__ is False


def test_silent_flag_inheritance() -> None:
    """
    Test script subcommand has silent disabled by default
    """
    script, _command = initialize_empty_command()
    script.__silent__ = True
    assert script.__is_silent__ is True
    for command in script.__subcommands__.values():
        assert command.__is_silent__ is True


def test_command_exit(capsys) -> None:
    """
    Test calling exit from command
    """
    _script, command = initialize_empty_command()
    message = 'Command exits'
    with pytest.raises(SystemExit) as exit_code:
        command.exit(1, message)
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_command_error(capsys) -> None:
    """
    Test calling error from command
    """
    _script, command = initialize_empty_command()
    message = 'Command exits'
    command.error(message)
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_command_message(capsys) -> None:
    """
    Test calling message from command
    """
    _script, command = initialize_empty_command()
    message = 'Command exits'
    command.message(message)
    captured = capsys.readouterr()
    assert message in captured.out.splitlines()


def test_command_message_silent(capsys) -> None:
    """
    Test calling mesasge from command with silent flag set
    """
    script, command = initialize_empty_command()
    script.__silent__ = True
    message = 'Command exits'
    command.message(message)
    captured = capsys.readouterr()
    assert captured.out == ''


def test_command_with_result(monkeypatch) -> None:
    """
    Test result command run is called
    """
    script = Script()
    command = ResultsCommand(script)
    script.add_subcommand(command)

    testargs = ('test', 'empty')
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', testargs)
        assert command.result is False
        with pytest.raises(SystemExit) as exit_status:
            script.run()
        assert exit_status.value.code == 0
        assert command.result is True


def test_command_with_invalid_args(monkeypatch) -> None:
    """
    Test result command run is called
    """
    script = Script()
    command = ResultsCommand(script)
    script.add_subcommand(command)

    testargs = ('test', 'invalid')
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', testargs)
        with pytest.raises(SystemExit) as exit_code:
            assert command.result is False
            script.run()
            assert command.result is False
        assert exit_code.value.code == 2
