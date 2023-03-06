#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Common methods for CLI command test cases
"""
import pytest

from cli_toolkit.base import Base, NestedCliCommand, ScriptError


def test_base_invalid_parent_class() -> None:
    """
    Test loading NestedCliCommand with invalid parent
    """
    with pytest.raises(TypeError):
        Base(parent={})


def test_no_name() -> None:
    """
    Test NestedCliCommand direct init without name
    """
    with pytest.raises(ScriptError):
        NestedCliCommand()


def test_nested_command_invalid_parent_class() -> None:
    """
    Test loading NestedCliCommand with invalid parent
    """
    with pytest.raises(TypeError):
        NestedCliCommand(parent={})
