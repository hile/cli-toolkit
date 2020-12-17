"""
Unit tests for configuration sections
"""

from pathlib import Path

import pytest

from cli_toolkit.configuration import ConfigurationList, ConfigurationSection
from cli_toolkit.exceptions import ConfigurationError

TEST_DEFAULT_DATA = {
    'test_key': 'test value',
    'nested_level_1': {
        'test_nested_key': 'test nested value'
    }
}

TEST_NESTED_LIST_DATA = {
    'nested_item_1': {
        'list_field': [
            {
                'list_nested_item': {
                    'field': 1234,
                }
            },
            'text list item'
        ]

    }
}

TEST_EMPTY_DATA = {
    'test_key_empty': '',
    'nested_level_1': {}
}

TEST_INVALID_VALUES = (
    (1, 'test numeric value'),
    ('spaced out', 'test invalid attr string'),
    ('dashed-string', 'test invalid dashed string'),
)


class EnvDefaultsConfigurationSection(ConfigurationSection):
    """
    Configuration with default settings and environment
    variables
    """
    __default_settings__ = {
        'test_key': 'test value'
    }
    __environment_variables__ = {
        'TEST_RESULT_KEY': 'test_key'
    }


class DefaultsConfigurationSection(ConfigurationSection):
    """
    Configuration with default variables
    """
    __default_settings__ = {
        'test_key': 'test value',
        'nested_default': {
            'test_nested_key': 'nested value'
        }
    }


class EnvConfigurationSection(ConfigurationSection):
    """
    Configuration with environment variables
    """
    __environment_variables__ = {
        'MY_TEST_KEY': 'test_key'
    }
    __environment_variable_prefix__ = 'PREFIXED'


class InvalidDefaultConfigurationSection(ConfigurationSection):
    """
    Configuration with invalid default settings
    """
    __default_settings__ = {
        'test key': 'test value'
    }


class InvalidEnvConfigurationSection(ConfigurationSection):
    """
    Configuration with invalid environment settings
    """
    __environment_variables__ = {
        'TEST_RESULT_KEY': 'test key'
    }


class NestedConfigurationSection(ConfigurationSection):
    """
    Nested configuration section
    """
    __name__ = 'nested'


class NestedDefaultConfigurationSection(ConfigurationSection):
    """
    Nested configuration section default for unnamed sections
    """


class NestedListConfigurationSection(ConfigurationSection):
    """
    Nested configuration section default for list sections
    """
    __name__ = 'lists'


class NestedRootConfigurationSection(ConfigurationSection):
    """
    NestedRoot configuration section for nested configurations
    """
    __dict_loader_class__ = NestedDefaultConfigurationSection
    __list_loader_class__ = NestedListConfigurationSection
    __section_loaders__ = (
        NestedConfigurationSection,
        NestedListConfigurationSection,
    )


class InvalidRootConfigurationSection(ConfigurationSection):
    """
    NestedRoot configuration section with base ConfigurationSection

    Causes error due to no section name
    """
    __section_loaders__ = (
        ConfigurationSection,
    )


class RequiredSettingsConfigurationSection(ConfigurationSection):
    """
    Configuration section with required settings
    """
    __required_settings__ = (
        'test_key',
    )


class FormattedConfigurationSection(ConfigurationSection):
    """
    Configuration with formatter callback
    """
    @staticmethod
    def format_test_key(value):
        """
        Format expected test key value
        """
        return value.upper()


class ValidatedConfigurationSection(ConfigurationSection):
    """
    Configuration with validator callback
    """
    @staticmethod
    def validate_test_key(value):
        """
        Validate expected test key value
        """
        return value


class InvalidatedConfigurationSection(ConfigurationSection):
    """
    Configuration with validator callback raising error
    """
    @staticmethod
    def validate_test_key(value):
        """
        Validate expected test key value
        """
        raise ValueError('Invalid value')


def validate_configuration_section(section, data, parent=None):
    """
    Validate configuration section details
    """
    assert section.__parent__ == parent

    for key, value in data.items():
        assert hasattr(section, key)
        if isinstance(value, dict):
            validate_configuration_section(
                getattr(section, key),
                value,
                section
            )
        else:
            assert getattr(section, key) == value


def test_configuration_section_default_empty():
    """
    Test loading empty configuration section without data
    """
    section = ConfigurationSection()
    assert isinstance(section.__section_loaders__, tuple)
    assert isinstance(section.__default_settings__, dict)
    assert isinstance(section.__required_settings__, (tuple, list))


def test_configuration_section_invalid_parent():
    """
    Test initializing configuration section with invalid parent
    """
    with pytest.raises(TypeError):
        ConfigurationSection(parent={})


def test_configuration_section_attribute_name():
    """
    Test validation of attribute names for configuration secrion
    """
    configuration = ConfigurationSection()

    for attr in ('test', 'test123'):
        configuration.__validate_attribute__(attr)

    with pytest.raises(ConfigurationError):
        configuration.__validate_attribute__('hähää')


def test_configuration_section_empty_data():
    """
    Test loading configuration section with empty values in data
    """
    configuration = ConfigurationSection(data=TEST_EMPTY_DATA)

    assert configuration.__config_root__ == configuration

    # pylint: disable=no-member
    assert configuration.test_key_empty is None

    with pytest.raises(ConfigurationError):
        configuration.__get_section_loader__('')

    assert configuration.__key_from_attribute__('test') == 'test'
    configuration.__key_attribute_map__ = {
        'other': 'match'
    }
    assert configuration.__key_from_attribute__('match') == 'other'
    assert configuration.__key_from_attribute__('other') == 'other'


def test_configuration_section_list_data():
    """
    Test loading configuration section with list of mixed content
    """
    configuration = ConfigurationSection(data=TEST_NESTED_LIST_DATA)
    # pylint: disable=no-member
    nested_item = configuration.nested_item_1
    assert isinstance(nested_item, ConfigurationSection)

    assert nested_item.__config_root__ == configuration

    list_value = nested_item.list_field
    assert isinstance(list_value.__repr__(), str)
    assert isinstance(list_value, ConfigurationList)
    assert len(list_value) == 2

    assert list_value.__config_root__ == configuration

    assert isinstance(list_value[0], ConfigurationSection)
    assert isinstance(list_value[1], str)

    for item in list_value:
        assert item is not None


def test_configuration_section_default_with_data():
    """
    Test loading default configuration section with test data
    """
    section = ConfigurationSection(data=TEST_DEFAULT_DATA)
    validate_configuration_section(section, TEST_DEFAULT_DATA)


def test_configuration_section_empty_set_invalid_values():
    """
    Test loading default configuration section with test data
    """
    section = ConfigurationSection()
    for item in TEST_INVALID_VALUES:
        with pytest.raises(ConfigurationError):
            section.set(item[0], item[1])

    for invalid_value in (None, [1, 2, 3]):
        with pytest.raises(ConfigurationError):
            section.__load_dictionary__(invalid_value)

        with pytest.raises(ConfigurationError):
            section.__load_section__('test', invalid_value)


def test_configuration_section_load_section_explicit():
    """
    Load new section explicitly
    """
    configuration = ConfigurationSection()
    configuration.__load_section__(
        'test',
        {'test_key': 'test value'}
    )
    # pylint: disable=no-member
    assert configuration.test.test_key == 'test value'


def test_configuration_section_load_section_nomatch_path():
    """
    Load new section with complex path
    """
    configuration = ConfigurationSection()

    configuration.__load_section__(
        'test',
        '123',
        path='other.bar.test_key'
    )
    # pylint: disable=no-member
    assert configuration.test.other.bar.test_key == '123'

    configuration.__load_section__(
        'test',
        {'test_key': 'test value'},
        path='other.sub.test_key'
    )
    # pylint: disable=no-member
    assert configuration.test.other.sub.test_key == 'test value'


def test_configuration_section_defaults():
    """
    Test configuration section with default settings
    """
    configuration = DefaultsConfigurationSection()
    assert len(configuration.__valid_settings__) == 1


def test_configuration_section_env(monkeypatch):
    """
    Test configuration section with environment settings
    """
    configuration = EnvConfigurationSection()
    assert len(configuration.__valid_settings__) == 1
    # pylint: disable=no-member
    assert configuration.test_key is None

    value = 'mock me env'
    with monkeypatch.context() as context:
        context.setenv('PREFIXED_TEST_KEY', value)
        configuration = EnvConfigurationSection()
        # pylint: disable=no-member
        assert configuration.test_key == value

    with monkeypatch.context() as context:
        context.setenv('MY_TEST_KEY', value)
        configuration = EnvConfigurationSection()
        # pylint: disable=no-member
        assert configuration.test_key == value


def test_configuration_section_env_defaults():
    """
    Test configuration section with default and environment settings
    """
    configuration = EnvDefaultsConfigurationSection()
    assert len(configuration.__valid_settings__) == 1
    # pylint: disable=no-member
    assert configuration.test_key == 'test value'


def test_configuration_section_invalid_defaults():
    """
    Test configuration section with invalid default settings
    """
    with pytest.raises(ConfigurationError):
        InvalidDefaultConfigurationSection()


def test_configuration_section_invalid_env():
    """
    Test configuration section with invalid environment settings
    """
    with pytest.raises(ConfigurationError):
        InvalidEnvConfigurationSection()


def test_configuration_section_nested_loader_unknown():
    """
    Test configuration sections with nested classes
    """
    configuration = ConfigurationSection()
    loader = configuration.__get_section_loader__('test')
    assert loader == ConfigurationSection

    configuration = NestedRootConfigurationSection()
    loader = configuration.__get_section_loader__(NestedConfigurationSection.__name__)
    assert loader == NestedConfigurationSection

    dict_output = configuration.as_dict()
    assert isinstance(dict_output, dict)


def test_configuration_section_nested_classes():
    """
    Test configuration sections with nested classes
    """
    configuration = NestedRootConfigurationSection()
    subsection = getattr(configuration, 'nested', None)
    assert subsection is not None
    assert isinstance(subsection, NestedConfigurationSection)
    assert subsection.__name__ == 'nested'

    assert configuration.__list_loader__ == NestedListConfigurationSection
    list_section = getattr(configuration, 'lists', None)
    assert list_section is not None
    assert isinstance(list_section, NestedListConfigurationSection)
    assert list_section.__name__ == 'lists'

    loader = configuration.__get_or_create_subsection__('unknown')
    assert loader.__name__ == 'unknown'

    configuration.__load_section__('test', {'test_key': 'test value'})
    # pylint: disable=no-member
    section = configuration.test
    assert isinstance(section, NestedDefaultConfigurationSection)
    assert section.test_key == 'test value'


def test_configuration_register_subsection_fail():
    """
    Test failure registering subsection without name
    """
    with pytest.raises(ConfigurationError):
        InvalidRootConfigurationSection()


def test_configuration_section_required_settings():
    """
    Test loading configuration section with required settings
    """
    section = RequiredSettingsConfigurationSection(data=TEST_DEFAULT_DATA)
    validate_configuration_section(section, TEST_DEFAULT_DATA)

    invalid_data = TEST_DEFAULT_DATA.copy()
    invalid_data['test_key'] = None
    with pytest.raises(ConfigurationError):
        RequiredSettingsConfigurationSection(data=invalid_data)

    with pytest.raises(ConfigurationError):
        RequiredSettingsConfigurationSection()


def test_configuration_section_paths():
    """
    Test loading configuration section with subsection paths
    """
    configuration = ConfigurationSection()
    section, field = configuration.__init_subsection_path__('test', 'test_field')
    assert section.__config_root__ == configuration
    assert section.__name__ == 'test'
    assert field == 'test_field'

    section, field = configuration.__init_subsection_path__('test', 'inner.value')
    assert section.__config_root__ == configuration
    assert isinstance(section, ConfigurationSection)
    assert section.__name__ == 'inner'
    assert section.__parent__.__name__ == 'test'
    assert field == 'value'

    configuration.__load_section__('sub', {'test': 'value'}, path='outer')
    assert configuration.sub.outer.test == 'value'

    configuration.__load_section__('sub', 'value', path='inner.test')
    assert configuration.sub.inner.test == 'value'


def test_configuration_section_load_dictionary():
    """
    Test loading dictionaries with __load_dictionary__ method using some more funky formats
    """
    configuration = ConfigurationSection()
    data = {
        'foo.bar': 'test',
        'bar.baz': {
            'zyxxy': 'item'
        }
    }
    configuration.__load_dictionary__(data)
    assert configuration.foo.bar == 'test'
    assert configuration.bar.baz.zyxxy == 'item'

    dict_output = configuration.as_dict()
    assert isinstance(dict_output, dict)


def test_configuration_section_set():
    """
    Test set() method of configuration section
    """
    configuration = ConfigurationSection()
    configuration.set('test', {'key': 'value'})
    assert configuration.test.key == 'value'
    configuration.set('foo.bar', 'baz')
    assert configuration.foo.bar == 'baz'


def test_configuration_section_set_formatters():
    """
    Test configuration section with number attribute formatters
    """
    configuration = ConfigurationSection()
    configuration.__integer_settings__ = ('integrity',)
    configuration.__float_settings__ = ('floating',)
    configuration.__path_settings__ = ('root',)

    configuration.set('test', {'a': 'a value'})
    assert isinstance(configuration.test, ConfigurationSection)
    assert configuration.test.a == 'a value'

    configuration.set('integrity', '123')
    assert configuration.integrity == 123
    configuration.set('floating', '123.25')
    assert configuration.floating == 123.25

    configuration.set('root', '/tmp')
    assert isinstance(configuration.root, Path)


def test_configuration_section_field_formatter_pass():
    """
    Test configuration section with custom formatter passing
    """
    configuration = FormattedConfigurationSection(data=TEST_DEFAULT_DATA)
    # pylint: disable=no-member
    assert configuration.test_key == 'TEST VALUE'

    with pytest.raises(ConfigurationError):
        FormattedConfigurationSection(data={'test_key': 123})


def test_configuration_section_field_validation_pass():
    """
    Test configuration section with custom validation passing
    """
    section = ValidatedConfigurationSection(data=TEST_DEFAULT_DATA)
    validate_configuration_section(section, TEST_DEFAULT_DATA)


def test_configuration_section_field_validation_fail():
    """
    Test configuration section with custom validation fails
    """
    with pytest.raises(ConfigurationError):
        InvalidatedConfigurationSection(data=TEST_DEFAULT_DATA)
