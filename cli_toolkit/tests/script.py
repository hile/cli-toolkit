"""
Common unit test validators for cli_toolkit.script.Script objects
"""

import argparse
import sys

import pytest

from ..script import Script


def validate_script_attributes(script,
                               expected_args,
                               formatter_class=None,
                               debug_enabled=False
                               ):
    """
    Validate common attributes of Script instance
    """
    assert isinstance(script, Script)

    assert script.__debug_enabled__ == debug_enabled

    if formatter_class is not None:
        assert script.__parser__.formatter_class == formatter_class
    else:
        assert script.__parser__.formatter_class == script.default_formatter_class

    args = script.parse_args()
    assert isinstance(args, argparse.Namespace)
    assert vars(args) == expected_args


def validate_script_error_exit_code(exception, exit_code=1):
    """
    Assert running script raises specified exit code
    """
    assert exception.type == SystemExit
    assert exception.value.code == exit_code
    return exception


def validate_script_run_exception_with_args(script, context, args, exit_code=2):
    """
    Validate exception raised by running script with specified invalid
    arguments
    """
    context.setattr(sys, 'argv', args)
    with pytest.raises(SystemExit) as exception:
        script.run()
    assert exception.value.code == exit_code


def validate_script_debug_flag_enabled(script, context, expected_args):
    """
    Validate debug flag is set by script correctly
    """
    script.add_argument('--test', action='store_true', help='Set test flag')
    expected_args['debug'] = True
    expected_args['test'] = True
    testargs = [sys.argv[0], '--debug', '--test']
    context.setattr(sys, 'argv', testargs)
    args = script.parse_args()
    assert vars(args) == expected_args


def validate_script_quiet_flag_enabled(script, context, expected_args):
    """
    Validate debug flag is set by script correctly
    """
    script.add_argument('--test', action='store_true', help='Set test flag')
    expected_args['quiet'] = True
    expected_args['test'] = True
    testargs = [sys.argv[0], '--quiet', '--test']
    context.setattr(sys, 'argv', testargs)
    args = script.parse_args()
    assert vars(args) == expected_args
