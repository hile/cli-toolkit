"""
Test shared  pytest mock fixtures
"""

import sys


# pylint: disable=unused-argument
def test_fixtures_cli_mock_argv(cli_mock_argv):
    """
    Test sys.argv is mocked
    """
    assert sys.argv == ['test-cli']
