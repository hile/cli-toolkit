"""
Shared fixtures for unit tests
"""

import sys

import pytest


@pytest.fixture
def cli_mock_argv(monkeypatch):
    """
    Fixture to set argv for argparse tests
    """
    arguments = ['test-cli']
    monkeypatch.setattr(sys, 'argv', arguments)
