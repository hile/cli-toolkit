"""
Unit tests for yaml format configuration files
"""

from pathlib import Path

import pytest

from cli_toolkit.configuration import (
    ConfigurationError,
    ConfigurationSection,
    YamlConfiguration,
)

from . import DATA_DIRECTORY, NONEXISTING_FILE
from .test_configuration_sections import (
    validate_configuration_section,
    TEST_DEFAULT_DATA
)

TEST_CONFIGURATIONS = Path(DATA_DIRECTORY, 'configuration')

TEST_EMPTY = TEST_CONFIGURATIONS.joinpath('test_empty.yml')
TEST_INVALID = TEST_CONFIGURATIONS.joinpath('test_invalid.yml')
TEST_VALID = TEST_CONFIGURATIONS.joinpath('test_valid.yml')


class DefaultsPathsConfiguration(YamlConfiguration):
    """
    Configuration file with valid default configurations
    """
    __default_paths__ = [TEST_VALID, NONEXISTING_FILE]


def test_configuration_yml_default_no_file():
    """
    Test loading default YAML class without file
    """
    configuration = YamlConfiguration()
    assert configuration.__repr__() == ''
    assert configuration.__path__ is None


def test_configuration_yml_empty_file():
    """
    Test loading empty YAML file
    """
    configuration = YamlConfiguration(TEST_EMPTY)
    assert isinstance(configuration, ConfigurationSection)
    assert configuration.__repr__() == TEST_EMPTY.name


def test_configuration_yml_nonexisting_file():
    """
    Test loading default YAML class with nonexisting file
    """
    configuration = YamlConfiguration(NONEXISTING_FILE)
    assert configuration.__repr__() == NONEXISTING_FILE.name
    assert configuration.__path__ == NONEXISTING_FILE


def test_configuration_yml_load_directory():
    """
    Test loading default YAML class with directory as path
    """
    with pytest.raises(ConfigurationError):
        YamlConfiguration(Path(__file__).parent)


# pylint: disable=unused-argument
def test_configuration_yml_load_inaccessible(tmpdir, mock_path_not_file):
    """
    Test loading default YAML class with inaccessible file
    """
    path = Path(tmpdir).joinpath('test.yml')
    with open(path, 'w') as filedescriptor:
        filedescriptor.write('---\n')

    with pytest.raises(ConfigurationError):
        YamlConfiguration(path)


# pylint: disable=unused-argument
def test_configuration_yml_load_permission_denied(tmpdir, mock_permission_denied):
    """
    Test loading default YAML class with no permissions to file
    """
    path = Path(tmpdir).joinpath('test.yml')
    with open(path, 'w') as filedescriptor:
        filedescriptor.write('---\n')

    with pytest.raises(ConfigurationError):
        YamlConfiguration(path)


def test_configuration_yml_invalid_file():
    """
    Test loading invalid YAML file
    """
    with pytest.raises(ConfigurationError):
        YamlConfiguration(TEST_INVALID)


def test_configuration_yml_valid_file():
    """
    Test loading valid YAML file
    """
    configuration = YamlConfiguration(TEST_VALID)
    assert isinstance(configuration, ConfigurationSection)
    validate_configuration_section(configuration, TEST_DEFAULT_DATA)


def test_configuration_yml_default_paths():
    """
    Test loading YAML configuration with default paths
    """
    configuration = DefaultsPathsConfiguration()
    validate_configuration_section(configuration, TEST_DEFAULT_DATA)
