"""
Pytest unit test configuration for cli_toolkit_demo

This example shows how to load cli_toolkit.fixtures shared fixtures
to unit tests for child modules
"""

import pytest


@pytest.fixture(autouse=True)
def common_fixtures(cli_mock_argv):
    """
    Wrap cli_mock_argv to be used in all tests from cli_toolkit.fixtures
    """
    print('mock CLI argv', cli_mock_argv)
