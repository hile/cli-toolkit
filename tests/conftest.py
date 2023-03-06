#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Pytest configuration for cli-toolkit unit tests
"""
import pytest


@pytest.fixture(autouse=True)
def common_fixtures(cli_mock_argv) -> None:
    """
    Wrap cli_mock_argv to be used in all tests
    """
    print('mock CLI argv', cli_mock_argv)
