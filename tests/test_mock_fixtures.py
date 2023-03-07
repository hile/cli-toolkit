#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Test shared  pytest mock fixtures
"""
import sys


def test_fixtures_cli_mock_argv(cli_mock_argv) -> None:
    """
    Test sys.argv is mocked
    """
    assert sys.argv == cli_mock_argv
