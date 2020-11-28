"""
Unit tests demo for running specific CLI commands with arguments, triggering
the subcommand class
"""

import sys

import pytest

from cli_toolkit_demo.bin.cli_demo.main import main


def test_cli_demo_config_no_args(capsys, monkeypatch):
    """
    Test running 'cli-demo config' command without additional arguments

    Since this command has no additional arguments this simply runs the script
    """
    argv = [
        'cli-demo',
        'config'
    ]
    monkeypatch.setattr(sys, 'argv', argv)
    # Runs the CLI command and returns without errors. This always raises SystemExit with status 0
    with pytest.raises(SystemExit) as exit_status:
        main()
    assert exit_status.value.code == 0
    captured = capsys.readouterr()
    assert captured.err == ''
