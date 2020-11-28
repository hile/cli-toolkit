"""
Unit tests demonstrating use of fixtures from cli-toolkit.fixtures for
testing base CLI argument handling

Demonstrates generic principles for writing unit tests for CLI commands:
- how to set the arguments to be tested
- how to call the entrypoint
- how to work with captured command line output in unit tests
"""

import sys

import pytest

from cli_toolkit_demo.bin.cli_demo.main import main, CLIDemo


def test_cli_demo_no_args(capsys, monkeypatch):
    """
    Test running command 'cli-demo without arguments'

    Since the command defines subcommands, this will exit with error

    This show Script's error handler and raises SystemExit with return code 1.
    This is standard argparse.ArgumentParser action.
    """
    # Note: argv must be list, not tuple. This is required by argparse.ArgumentParser
    argv = [
        'cli-demo',
    ]
    monkeypatch.setattr(sys, 'argv', argv)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 1

    captured = capsys.readouterr()
    # Command outputs nothing to stderr
    assert captured.out == ''

    # Command outputs lines to stderr
    stderr_lines = captured.err.splitlines()

    # Note: this output is not visible unless test case fails. It may still be useful to
    # print it out in case unit test fails to debug what was the unexpected output
    for line in stderr_lines:
        print(f'error {line}')
    assert len(stderr_lines) == 1

    # This line comes from base class and can be overriden in class variables if required
    assert stderr_lines[0] == CLIDemo.no_subcommand_error


def test_cli_demo_help(monkeypatch):
    """
    Test running command 'cli-demo --help'

    The --help flag shows utility help message and raises SystemExit with return code 0.
    This is standard argparse.ArgumentParser action.
    """
    # Note: argv must be list, not tuple. This is required by argparse.ArgumentParser
    argv = [
        'cli-demo',
        '--help'
    ]
    monkeypatch.setattr(sys, 'argv', argv)
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
