"""
Pytest configuration for cli-toolkit unit tests
"""

import pytest


@pytest.fixture(autouse=True)
def common_fixtures(cli_mock_argv):
    """
    Wrap cli_mock_argv to be used in all tests
    """
    print('mock CLI argv', cli_mock_argv)
