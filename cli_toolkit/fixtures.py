"""
Shared fixtures for unit tests
"""

import os
import sys

from pathlib import Path

import pytest


@pytest.fixture
def cli_mock_argv(monkeypatch):
    """
    Fixture to set argv for argparse tests
    """
    arguments = ['test-cli']
    monkeypatch.setattr(sys, 'argv', arguments)


@pytest.fixture
def mock_path_mkdir_permission_denied(monkeypatch):
    """
    Fixture to mock pathlib.Path.exists to return false
    """
    # pylint: disable=unused-argument
    def permission_error(*args, **kwargs):
        """
        Always return false for os.access
        """
        raise OSError('Permission denied')

    monkeypatch.setattr(Path, 'mkdir', permission_error)


@pytest.fixture
def mock_path_not_exists(monkeypatch):
    """
    Fixture to mock pathlib.Path.exists to return false
    """
    # pylint: disable=unused-argument
    def not_exists(*args):
        """
        Always return false for os.access
        """
        return False

    monkeypatch.setattr(Path, 'exists', not_exists)


@pytest.fixture
def mock_path_not_file(monkeypatch):
    """
    Fixture to mock pathlib.Path.is_file to return false
    """
    # pylint: disable=unused-argument
    def not_is_file(*args):
        """
        Always return false for is_file
        """
        return False

    monkeypatch.setattr(Path, 'is_file', not_is_file)


@pytest.fixture
def mock_permission_denied(monkeypatch):
    """
    Fixture to mock os.access returning false
    """
    # pylint: disable=unused-argument
    def permission_denied(*args):
        """
        Always return false for os.access
        """
        return False

    monkeypatch.setattr(os, 'access', permission_denied)
