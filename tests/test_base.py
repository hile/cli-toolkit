"""
Common methods for CLI command test cases
"""

import pytest

from cli_toolkit.base import Base, NestedCliCommand, ScriptError


def test_base_invalid_parent_class():
    """
    Test loading NestedCliCommand with invalid parent
    """
    with pytest.raises(TypeError):
        Base(parent={})


def test_no_name():
    """
    Test NestedCliCommand direct init without name
    """
    with pytest.raises(ScriptError):
        NestedCliCommand()


def test_nested_command_invalid_parent_class():
    """
    Test loading NestedCliCommand with invalid parent
    """
    with pytest.raises(TypeError):
        NestedCliCommand(parent={})
