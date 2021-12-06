"""
Unit tests for JSON format configuration files
"""

from pathlib import Path

import pytest

from cli_toolkit.configuration import (
    ConfigurationError,
    ConfigurationSection,
    JsonConfiguration,
)

from . import DATA_DIRECTORY, NONEXISTING_FILE
from .test_configuration_sections import (
    validate_configuration_section,
    TEST_DEFAULT_DATA
)

TEST_CONFIGURATIONS = Path(DATA_DIRECTORY, 'configuration')

TEST_EMPTY = TEST_CONFIGURATIONS.joinpath('test_empty.json')
TEST_INVALID = TEST_CONFIGURATIONS.joinpath('test_invalid.json')
TEST_VALID = TEST_CONFIGURATIONS.joinpath('test_valid.json')


class DefaultsPathsConfiguration(JsonConfiguration):
    """
    Configuration file with valid default configurations
    """
    __default_paths__ = [TEST_VALID, NONEXISTING_FILE]


def test_configuration_json_default_no_file():
    """
    Test loading default JSON class without file
    """
    configuration = JsonConfiguration()
    assert configuration.__repr__() == ''
    assert configuration.__path__ is None


def test_configuration_json_nonexisting_file():
    """
    Test loading default JSON class with nonexisting file
    """
    configuration = JsonConfiguration(NONEXISTING_FILE)
    assert configuration.__repr__() == NONEXISTING_FILE.name
    assert configuration.__path__ == NONEXISTING_FILE


def test_configuration_json_empty_file():
    """
    Test loading empty (but valid) JSON file
    """
    configuration = JsonConfiguration(TEST_EMPTY)
    assert isinstance(configuration, ConfigurationSection)
    assert configuration.__repr__() == TEST_EMPTY.name


def test_configuration_json_load_directory():
    """
    Test loading default JSON class with directory as path
    """
    with pytest.raises(ConfigurationError):
        JsonConfiguration(Path(__file__).parent)


# pylint: disable=unused-argument
def test_configuration_ini_load_inaccessible(tmpdir, mock_path_not_file):
    """
    Test loading default JSON class with inaccessible file
    """
    path = Path(tmpdir).joinpath('test.json')
    with path.open('w', encoding='utf-8') as filedescriptor:
        filedescriptor.write('{ "test": "value"}\n')
    with pytest.raises(ConfigurationError):
        JsonConfiguration(path)


# pylint: disable=unused-argument
def test_configuration_ini_load_permission_denied(tmpdir, mock_permission_denied):
    """
    Test loading default JSON class with no permissions to file
    """
    path = Path(tmpdir).joinpath('test.json')
    with path.open('w', encoding='utf-8') as filedescriptor:
        filedescriptor.write('{ "test": "value"}\n')
    with pytest.raises(ConfigurationError):
        JsonConfiguration(path)


def test_configuration_yml_invalid_file():
    """
    Test loading invalid JSON file
    """
    with pytest.raises(ConfigurationError):
        JsonConfiguration(TEST_INVALID)


def test_configuration_json_valid_file():
    """
    Test loading valid JSON file
    """
    configuration = JsonConfiguration(TEST_VALID)
    assert isinstance(configuration, ConfigurationSection)
    validate_configuration_section(configuration, TEST_DEFAULT_DATA)


def test_configuration_json_default_paths():
    """
    Test loading JSON configuration with default paths
    """
    configuration = DefaultsPathsConfiguration()
    validate_configuration_section(configuration, TEST_DEFAULT_DATA)
