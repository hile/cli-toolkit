"""
Unit tests for cli_toolkit.process module
"""

import os

from pathlib import Path

import pytest

from cli_toolkit.base import ScriptError
from cli_toolkit.process import run_command, run_command_lineoutput

MIXED__ENCODINGS_FILE = Path(__file__).parent.joinpath('data/linefile_mixed_encodings')


def verify_string_list(value):
    """
    Test specified value is list of strings
    """
    assert isinstance(value, list)
    for line in value:
        assert isinstance(line, str)


def test_run_command_uname_as_string():
    """
    Test running uname command
    """
    stdout, stderr = run_command('uname')
    assert isinstance(stdout, bytes)
    assert isinstance(stderr, bytes)


def test_run_command_uname_with_env_path():
    """
    Test running uname command with custom invalid PATH

    Fails because command is not on path
    """
    env = os.environ.copy()
    env['PATH'] = '/foo:/bar'
    with pytest.raises(ScriptError):
        run_command('uname', env=env)


def test_run_command_uname_as_args_list():
    """
    Test running uname command
    """
    args = ['uname']
    stdout, stderr = run_command(*args)
    assert isinstance(stdout, bytes)
    assert isinstance(stderr, bytes)


def test_run_command_uname_as_args_tuple():
    """
    Test running uname command
    """
    args = ['uname']
    stdout, stderr = run_command(*args)
    assert isinstance(stdout, bytes)
    assert isinstance(stderr, bytes)


def test_run_command_running_explicit_return_codes():
    """
    Test running an command by specifying list of
    expected return codes
    """
    args = ['uname']
    stdout, stderr = run_command_lineoutput(*args, expected_return_codes=[0])
    assert isinstance(stdout, list)
    assert isinstance(stderr, list)


def test_run_command_timeout_exceeded():
    """
    Test running an command raising timeout
    """
    args = ['sleep', '1']
    run_command_lineoutput(*args, timeout=2)
    args = ['sleep', '5']
    with pytest.raises(ScriptError):
        run_command_lineoutput(*args, timeout=0.5)


def test_run_command_with_invalid_args():
    """
    Test running an invalid command
    """
    with pytest.raises(ScriptError):
        run_command('uname', '--foobar')


def test_run_command_running_invalid_command():
    """
    Test running an invalid command
    """
    with pytest.raises(ScriptError):
        run_command('49FC61D4-F21B-4A0D-941D-9CC52F163CFF')


def test_process_running_command_with_invalid_args():
    """
    Test running an invalid command
    """
    with pytest.raises(ScriptError):
        run_command('uname', '--foobar')


def test_process_running_invalid_command():
    """
    Test running an invalid command
    """
    with pytest.raises(ScriptError):
        run_command('49FC61D4-F21B-4A0D-941D-9CC52F163CFF')


def test_process_lineoutput_running_uname_as_string():
    """
    Test running uname command
    """
    stdout, stderr = run_command_lineoutput('uname')
    verify_string_list(stdout)
    verify_string_list(stderr)


def test_process_lineoutput_running_uname_as_args_list():
    """
    Test running uname command
    """
    args = [
        'uname',
    ]
    stdout, stderr = run_command_lineoutput(*args)
    verify_string_list(stdout)
    verify_string_list(stderr)


def test_process_lineoutput_running_uname_as_args_tuple():
    """
    Test running uname command
    """
    args = (
        'uname',
    )
    stdout, stderr = run_command_lineoutput(*args)
    verify_string_list(stdout)
    verify_string_list(stderr)


def test_process_lineoutput_mixed_encoding_file_read():
    """
    Unit tests for reading a file with mixed encodings
    """
    command = ('cat', MIXED__ENCODINGS_FILE.absolute())
    with pytest.raises(ScriptError):
        run_command_lineoutput(*command)

    encodings = ['utf-8', 'latin1']
    stdout, stderr = run_command_lineoutput(*command, encodings=encodings)
    assert len(stdout) == 2
    assert len(stderr) == 0
    for line in stdout:
        assert isinstance(line, str)
