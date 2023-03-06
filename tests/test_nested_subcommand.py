#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Unit tests for cli_toolkit.command nested subcommands
"""
import sys

from argparse import Namespace

import pytest

from sys_toolkit.tests.mock import MockCalledMethod, MockReturnFalse, MockReturnTrue

from cli_toolkit.script import Script
from cli_toolkit.command import Command


class ThirdLevelCommand(Command):
    """
    3rd level test sub command
    """
    name = 'thirdlevel'
    parsed = False
    result = False

    def parse_args(self, args: Namespace = None, namespace: Namespace = None) -> Namespace:
        """
        Parse subcommand args
        """
        self.parsed = True
        return args

    def run(self, args: Namespace) -> None:
        """
        Run subcommand
        """
        self.result = True


class SecondLevelCommand(Command):
    """
    2nd level test sub command
    """
    name = 'secondlevel'
    subcommands = (
        ThirdLevelCommand,
    )


class FirstLevelCommand(Command):
    """
    1st level test sub command
    """
    name = 'firstlevel'
    subcommands = (
        SecondLevelCommand,
    )


def test_nested_subcommands_create(monkeypatch) -> None:
    """
    Test adding command without name
    """
    script = Script()
    command = FirstLevelCommand(script)
    script.add_subcommand(command)

    first = script.__subcommands__['firstlevel']
    second = first.__subcommands__['secondlevel']
    third = second.__subcommands__['thirdlevel']

    assert third.parsed is False
    assert third.result is False

    argv = ['test', 'firstlevel', 'secondlevel', 'thirdlevel']
    monkeypatch.setattr(sys, 'argv', argv)
    with pytest.raises(SystemExit) as exit_status:
        script.run()
    assert exit_status.value.code == 0
    assert third.parsed is True
    assert third.result is True


def test_nested_subcommand_stty_flush_with_tty(monkeypatch) -> None:
    """
    Test using nested_subcommand  with stty flush after command finishes
    """
    script = Script()
    command = FirstLevelCommand(script)
    script.add_subcommand(command)

    mock_system_command = MockCalledMethod()
    mock_return_true = MockReturnTrue()
    monkeypatch.setattr('os.system', mock_system_command)
    monkeypatch.setattr('sys.platform', 'bsd')
    monkeypatch.setattr('sys.stdin.isatty', mock_return_true)
    argv = ['test', 'firstlevel', 'secondlevel', 'thirdlevel']
    monkeypatch.setattr(sys, 'argv', argv)
    with pytest.raises(SystemExit):
        script.run()
    assert mock_system_command.call_count == 1


def test_nested_subcommand_stty_flush_no_tty(monkeypatch) -> None:
    """
    Test using nested_subcommand  with stty flush after command finishes
    """
    script = Script()
    command = FirstLevelCommand(script)
    script.add_subcommand(command)

    mock_system_command = MockCalledMethod()
    mock_return_false = MockReturnFalse()
    monkeypatch.setattr('os.system', mock_system_command)
    monkeypatch.setattr('sys.platform', 'bsd')
    monkeypatch.setattr('sys.stdin.isatty', mock_return_false)
    argv = ['test', 'firstlevel', 'secondlevel', 'thirdlevel']
    monkeypatch.setattr(sys, 'argv', argv)
    with pytest.raises(SystemExit):
        script.run()
    assert mock_system_command.call_count == 0


def test_nested_subcommand_win32_no_stty_flush(monkeypatch) -> None:
    """
    Test using nested_subcommand wihtout stty flush after command finishes
    """
    script = Script()
    command = FirstLevelCommand(script)
    script.add_subcommand(command)

    mock_system_command = MockCalledMethod()
    monkeypatch.setattr('os.system', mock_system_command)
    monkeypatch.setattr('sys.platform', 'win32')
    argv = ['test', 'firstlevel', 'secondlevel', 'thirdlevel']
    monkeypatch.setattr(sys, 'argv', argv)
    with pytest.raises(SystemExit):
        script.run()
    assert mock_system_command.call_count == 0
