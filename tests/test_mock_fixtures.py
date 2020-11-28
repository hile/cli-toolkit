"""
Test shared  mock  fixtures
"""

import os
import sys

from pathlib import Path


# pylint: disable=unused-argument
def test_fixtures_cli_mock_argv(cli_mock_argv):
    """
    Test sys.argv is mocked
    """
    assert sys.argv == ['test-cli']


# pylint: disable=unused-argument
def test_fixtures_mock_path_not_exists(mock_path_not_exists):
    """
    Test pathlib.Path.exists() returns always false
    """
    assert Path(__file__).exists() is False


# pylint: disable=unused-argument
def test_fixtures_mock_path_not_is_file(mock_path_not_file):
    """
    Test pathlib.Path.is_file() returns always false
    """
    assert Path(__file__).is_file() is False


# pylint: disable=unused-argument
def test_fixtures_mock_permission_denied(mock_permission_denied):
    """
    Test pathlib.Path.is_file() returns always false
    """
    assert os.access(__file__, os.R_OK) is False
