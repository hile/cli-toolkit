"""
Unit tests for cli_toolkit_demo.configuration module
"""

from cli_toolkit_demo.configuration import Configuration


def test_configuration_init():
    """
    Unit tests for loading demo configuration without parsing system or user configuration files
    """
    config = Configuration()
    # All configuration classes have these shared flags
    assert config.__debug_enabled__ is False
    assert config.__silent__ is False
