"""
Unit test utilities for pytest

This module implements repeated unit test validators used by this and other modules
"""

from packaging import version


def validate_version_string(value):
    """
    Ensure version string is valid

    Expects version string is a semantic version of numbers separate by .
    """
    parsed = version.parse(value)
    assert len(parsed.release) > 1
    for part in parsed.release:
        assert isinstance(part, int)
        assert part >= 0
