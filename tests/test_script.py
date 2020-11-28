
import argparse
import os
import signal
import sys
from unittest.mock import patch

import pytest

from cli_toolkit.script import Script
from cli_toolkit.tests.script import (
    validate_script_attributes,
    validate_script_debug_flag_enabled,
    validate_script_error_exit_code,
    validate_script_run_exception_with_args,
    validate_script_quiet_flag_enabled,
)

DEFAULT_ARGS = {
    'debug': False,
    'quiet': False
}


# pylint: disable=too-few-public-methods
class MockOsError:
    """
    Mock calls with OSError
    """
    def __init__(self):
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        """
        raise OSError
        """
        self.call_count += 1
        raise OSError(f'Mocked OSError {args} {kwargs}')


def test_script_create_empty():
    """
    Test creating script with no specific options
    """
    validate_script_attributes(
        Script(),
        expected_args=DEFAULT_ARGS
    )


def test_script_create_empty_with_formatter_class():
    """
    Test creating script with custom formatter class
    """
    formatter_class = argparse.MetavarTypeHelpFormatter
    validate_script_attributes(
        Script(formatter_class=formatter_class),
        expected_args=DEFAULT_ARGS,
        formatter_class=formatter_class
    )


def test_script_create_empty_custom_args():
    """
    Test creating script with no specific options
    """
    script = Script()
    script.add_argument('files', nargs='*', help='Add files')
    expected_args = DEFAULT_ARGS.copy()
    expected_args['files'] = []
    validate_script_attributes(
        script,
        expected_args=expected_args
    )


def test_script_no_subcommand_run():
    """
    Ensure empty script run() exits with code 1
    """
    script = Script()
    with pytest.raises(SystemExit) as exception:
        script.run()
    validate_script_error_exit_code(exception)


def test_script_reset_error(monkeypatch):
    """
    Test script running with error running stty reset
    """
    script = Script()
    mock_method = MockOsError()
    monkeypatch.setattr('os.system', mock_method)
    script.reset_stty()
    assert mock_method.call_count > 0


def test_script_sigint_handler():
    """
    Ensure empty script run() calls sigint handler with SIGINT
    """
    script = Script()
    with pytest.raises(SystemExit) as exception:
        with patch.object(script, 'SIGINT') as signal_handler:
            os.kill(os.getpid(), signal.SIGINT)
        assert signal_handler.called
    validate_script_error_exit_code(exception)


def test_script_with_invalid_args(monkeypatch):
    """
    Test running script with invalid arguments
    """
    script = Script()
    testargs = (sys.argv[0], 'invalid')
    with monkeypatch.context() as context:
        validate_script_run_exception_with_args(
            script,
            context,
            args=testargs,
        )


def test_script_with_debug_enabled(monkeypatch):
    """
    Test setting --debug flag
    """
    script = Script()
    with monkeypatch.context() as context:
        validate_script_debug_flag_enabled(
            script,
            context,
            expected_args=DEFAULT_ARGS.copy()
        )


def test_script_with_quiet_enabled(monkeypatch):
    """
    Test setting --quiet flag
    """
    script = Script()
    with monkeypatch.context() as context:
        validate_script_quiet_flag_enabled(
            script,
            context,
            expected_args=DEFAULT_ARGS.copy()
        )


def test_exit_no_message(capsys):
    """
    Test exit without message
    """
    script = Script()
    with pytest.raises(SystemExit) as exit_code:
        script.exit(-1)
    assert exit_code.value.code == 1
    captured = capsys.readouterr()
    assert captured.err == ''


def test_exit_with_invalid_value(capsys):
    """
    Test exit by sending invalid exit codes
    """
    script = Script()
    script.__debug_enabled__ = False
    message = 'Test silent debug message'
    with pytest.raises(SystemExit) as exit_code:
        script.exit(-1, message)
    assert exit_code.value.code == 1
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()

    with pytest.raises(SystemExit) as exit_code:
        script.exit('perkele', message)
    assert exit_code.value.code == 1
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_exit_with_bool_false(capsys):
    """
    Test exit by sending True to error code
    """
    script = Script()
    script.__debug_enabled__ = False
    message = 'Test silent debug message'
    with pytest.raises(SystemExit) as exit_code:
        script.exit(False, message)
    assert exit_code.value.code == 1
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_exit_with_bool_true(capsys):
    """
    Test exit by sending True to error code
    """
    script = Script()
    script.__debug_enabled__ = False
    message = 'Test silent debug message'
    with pytest.raises(SystemExit) as exit_code:
        script.exit(True, message)
    assert exit_code.value.code == 0
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_debug_message_disabled(capsys):
    """
    Test sending debug message with debug disabled
    """
    script = Script()
    script.__debug_enabled__ = False
    message = 'Test silent debug message'
    script.debug(message)
    captured = capsys.readouterr()
    assert captured.err == ''


def test_debug_message_enabled(capsys):
    """
    Test sending debug message with debug enabled
    """
    script = Script()
    script.__debug_enabled__ = True
    message = 'Test silent debug message'
    script.debug(message)
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_error_message_silent(capsys):
    """
    Test sending error message with silent flag
    """
    script = Script()
    message = 'Test error message with silent flag'
    script.__silent__ = True
    script.error(message)
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_error_message(capsys):
    """
    Test sending error message
    """
    script = Script()
    message = 'Test error message'
    script.error(message)
    captured = capsys.readouterr()
    assert message in captured.err.splitlines()


def test_message_silent(capsys):
    """
    Test sending message with silent flag
    """
    script = Script()
    message = 'Test message with silent flag'
    script.__silent__ = True
    script.message(message)
    captured = capsys.readouterr()
    assert captured.err == ''
