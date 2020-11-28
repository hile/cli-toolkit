"""
Unit test to validate version of python package
"""

from cli_toolkit.tests import validate_version_string

from cli_toolkit_demo import __version__


def test_version_string():
    """
    Test format of module version string
    """
    validate_version_string(__version__)
