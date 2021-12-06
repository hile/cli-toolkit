
import sys

import pytest

from cli_toolkit.script import Script
from cli_toolkit.command import Command


class ThirdLevelCommand(Command):
    """
    3rd level test sub command
    """
    name = 'thirdlevel'
    parsed = False
    result = False

    def parse_args(self, args=None, namespace=None):
        """
        Parse subcommand args
        """
        self.parsed = True
        return args

    def run(self, args):
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


def test_create_nested_subcommands(monkeypatch):
    """
    Test adding command without name
    """
    script = Script()
    command = FirstLevelCommand(script)
    script.add_subcommand(command)

    print('script', script.__subcommands__)
    first = script.__subcommands__['firstlevel']
    print('first level', first.__subcommands__)
    second = first.__subcommands__['secondlevel']
    print('seccnd level', second.__subcommands__)
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
