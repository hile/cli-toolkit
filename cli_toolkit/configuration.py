"""
Loaders for ini, json and yaml format configuration files
"""

import configparser
import json
import os
import re

from pathlib import Path

import yaml

from sys_toolkit.logger import DEFAULT_TARGET_NAME

from .base import Base
from .exceptions import ConfigurationError

# Pattern to validate configuration keys
RE_CONFIGURATIION_KEY = re.compile('^[a-zA-Z0-9_]+$')


class ConfigurationItemContainer(Base):
    """
    Base class for containers of settings
    """
    __dict_loader_class__ = None
    __list_loader_class__ = None
    __float_settings__ = ()
    """Tuple of settings loaded as floats"""
    __integer_settings__ = ()
    """Tuple of settings loaded as integers"""
    __path_settings__ = ()
    """Tuple of settings loaded as pathlib.Path"""

    def __init__(self, parent=None, debug_enabled=False, silent=False, logger=DEFAULT_TARGET_NAME):
        self.__attributes__ = []
        super().__init__(parent, debug_enabled, silent, logger)

    @property
    def __config_root__(self):
        """
        Return configuration root item via parent links
        """
        parent = getattr(self, '__parent__', None)
        if parent is None:
            return self
        while getattr(parent, '__parent__', None) is not None:
            parent = getattr(parent, '__parent__', None)
        return parent

    @property
    def __dict_loader__(self):
        """
        Return loader for dict items
        """
        if self.__dict_loader_class__ is not None:
            return self.__dict_loader_class__
        return ConfigurationSection

    @property
    def __list_loader__(self):
        """
        Return loader for list items
        """
        if self.__list_loader_class__ is not None:
            return self.__list_loader_class__
        return ConfigurationList

    @staticmethod
    def default_formatter(value):
        """
        Default formatter for variables

        By default trims whitespace from strings and sets empty strings to None
        """
        if isinstance(value, str):
            value = value.strip()
            if value == '':
                value = None
        return value

    @staticmethod
    def __validate_attribute__(attr):
        """
        Validate attribute to be set
        """
        if not isinstance(attr, str):
            raise ConfigurationError(f'Attribute is not string: {attr}')
        if not attr.isidentifier():
            raise ConfigurationError(f'Attribute is not valid python identifier: {attr}')
        if not RE_CONFIGURATIION_KEY.match(attr):
            raise ConfigurationError(f'Invalid attribute name: {attr}')

    def as_dict(self):
        """
        Return VS code configuration section as dictionary
        """
        data = {}
        for attribute in self.__attributes__:
            item = getattr(self, attribute)
            if hasattr(item, 'as_dict'):
                data[attribute] = item.as_dict()
            else:
                data[attribute] = item
        return data

    def set(self, attr, value):
        """
        Load item with correct class
        """
        self.__validate_attribute__(attr)

        section = getattr(self, attr, None)
        if section is not None and callable(getattr(section, 'set', None)):
            section.set(attr, value)
            return

        if isinstance(value, dict):
            item = self.__dict_loader__(value, parent=self)  # pylint: disable=not-callable
            setattr(self, attr, item)
            self.__attributes__.append(attr)
            return

        if isinstance(value, (list, tuple)):
            item = self.__list_loader__(attr, value, parent=self)  # pylint: disable=not-callable
            setattr(self, item.__setting__, item)
            self.__attributes__.append(item.__setting__)
            return

        if value is not None:
            if attr in self.__float_settings__:
                value = float(value)
            if attr in self.__integer_settings__:
                value = int(value)
            if attr in self.__path_settings__:
                value = Path(value).expanduser()

        validator_callback = getattr(self, f'validate_{attr}', None)
        if callable(validator_callback):
            try:
                value = validator_callback(value)  # pylint: disable=not-callable
            except Exception as error:
                raise ConfigurationError(f'Error validating setting {attr}: {error}') from error

        formatter_callback = getattr(self, f'format_{attr}', None)
        try:
            if callable(formatter_callback):
                value = formatter_callback(value)  # pylint: disable=not-callable
            else:
                value = self.default_formatter(value)
        except Exception as error:
            raise ConfigurationError(f'Error formatting setting {attr}: {error}') from error

        setattr(self, attr, value)
        self.__attributes__.append(attr)


class ConfigurationList(ConfigurationItemContainer):
    """
    List of settings in configuration section
    """
    def __init__(self, setting=None, data=None, parent=None):
        super().__init__(parent=parent)
        self.__setting__ = setting
        self.__load__(data)

    def __repr__(self):
        return self.__values__.__repr__()

    def __getitem__(self, index):
        return self.__values__[index]

    def __iter__(self):
        return iter(self.__values__)

    def __len__(self):
        return len(self.__values__)

    def __load__(self, value):
        """
        Load list of values
        """
        self.__values__ = []
        if value:
            for item in value:
                if isinstance(item, dict):
                    # pylint: disable=not-callable
                    item = self.__dict_loader__(item, parent=self)
                self.__values__.append(item)

    def set(self, attr, value):
        self.__load__(value)


class ConfigurationSection(ConfigurationItemContainer):
    """
    Configuration section with validation

    Configuration sections can be nested and linked to parent configuration
    section by parent argument. If parent is given it must be an instance of
    ConfigurationSection.

    Any data given in data dictionary are inserted as settings.
    """
    __name__ = None
    """Name of configuration section, used in linking custom classes"""
    __default_settings__ = {}
    """Dictionary of default settings configuration"""
    __required_settings__ = ()
    """Tuple of settings required for valid configuration"""
    __environment_variables__ = {}
    """Mapping from environment variables read to settings"""
    __environment_variable_prefix__ = None
    """Prefix for reading settings from environment variables"""

    __section_loaders__ = ()
    """Classes used for subsection parsers"""
    __key_attribute_map__ = {}
    """Map configuration keys to python compatible attributes"""

    def __init__(self, data=dict, parent=None, debug_enabled=False, silent=False):
        if parent is not None and not isinstance(parent, ConfigurationItemContainer):
            raise TypeError('parent must be instance of ConfigurationItemContainer')
        super().__init__(
            parent=parent,
            debug_enabled=debug_enabled,
            silent=silent,
        )

        self.__subsections__ = []

        self.__valid_settings__ = self.__detect_valid_settings__()
        for attr in self.__valid_settings__:
            self.set(attr, None)

        self.__initialize_sub_sections__()
        self.__load_dictionary__(self.__default_settings__)
        if isinstance(data, dict):
            self.__load_dictionary__(data)

        self.__load_environment_variables__()

        if parent is None:
            self.validate()

    def __repr__(self):
        return self.__name__ if self.__name__ is not None else ''

    def __initialize_sub_sections__(self):
        """
        Initialize sub sections configured in __section_loaders__
        """
        for loader in self.__section_loaders__:
            subsection = loader(data=None, parent=self)
            name = self.__attribute_from_key__(subsection.__name__)
            if name is None:
                raise ConfigurationError(f'Subsection class defines no name: {loader}')
            setattr(self, name, subsection)
            self.__attributes__.append(name)

    def __attribute_from_key__(self, key):
        """
        Map settings key to python attribute
        """
        return self.__key_attribute_map__.get(key, key)

    def __key_from_attribute__(self, attr):
        """
        Map settings file key from attribute
        """
        for key, value in self.__key_attribute_map__.items():
            if attr == value:
                return key
        return attr

    def __split_attribute_path__(self, key):
        """
        Return section attribute from key
        """
        key = self.__attribute_from_key__(key)
        if isinstance(key, str):
            parts = key.split('.')
            return parts[0], '.'.join(parts[1:])
        return key, []

    def __detect_valid_settings__(self):
        """
        Detect all known settings, return list of keys
        """
        attributes = []
        attributes = list(self.__required_settings__)
        for attr, value in self.__default_settings__.items():
            if not RE_CONFIGURATIION_KEY.match(attr):
                raise ConfigurationError(f'Invalid attribute name: {attr}')
            if not isinstance(value, dict) and attr not in attributes:
                attributes.append(attr)
        for attr in self.__environment_variables__.values():
            if not RE_CONFIGURATIION_KEY.match(attr):
                raise ConfigurationError(f'Invalid attribute name: {attr}')
            if attr not in attributes:
                attributes.append(attr)
        return sorted(set(attributes))

    def __load_environment_variables__(self):
        """
        Load settings from environment variables
        """
        if self.__environment_variable_prefix__ is not None:
            for attr in self.__valid_settings__:
                env = f'{self.__environment_variable_prefix__}_{attr}'.upper()
                value = os.environ.get(env, None)
                if value is not None:
                    self.set(attr, value)

        for env, attr in self.__environment_variables__.items():
            value = os.environ.get(env, None)
            if value is not None:
                self.set(attr, value)

    def __get_section_loader__(self, section_name):
        """
        Find configuration section loader by name

        By default returns ConfigurationSection
        """
        if not isinstance(section_name, str) or section_name == '':
            raise ConfigurationError('Configuration section name not defined')

        section_name = self.__attribute_from_key__(section_name)
        for loader in self.__section_loaders__:
            loader_name = self.__attribute_from_key__(getattr(loader, '__name__', None))
            if loader_name == section_name:
                return loader
        return self.__dict_loader__

    def __get_or_create_subsection__(self, name, parent=None):
        if parent is None:
            parent = self
        if not hasattr(parent, name):
            loader = parent.__get_section_loader__(name)
            item = loader({}, parent=parent)
            item.__name__ = name
            setattr(parent, name, item)
            parent.__subsections__.append(item)
        return getattr(parent, name)

    def __init_subsection_path__(self, section_name, path):
        """
        Initialize subsections from config path

        Splits . separated path to config setting path, creates subsections
        on path excluding last component

        Returns subsection matching longest path and field (last path component).
        Field is not actually loaded as the dictionary key
        """
        subsection = self.__get_or_create_subsection__(section_name)
        path = path.split('.')
        field = path[-1]
        if len(path) > 1:
            for subsection_name in path[:-1]:
                subsection = self.__get_or_create_subsection__(
                    subsection_name,
                    parent=subsection
                )
        return subsection, field

    def __load_section__(self, section, data, path=None):
        """
        Load configuration section from data
        """
        if path is not None:
            subsection, item = self.__init_subsection_path__(section, path)
            if isinstance(data, dict):
                if item == path:
                    subsection = self.__get_or_create_subsection__(
                        item,
                        parent=subsection
                    )
                subsection.__load_dictionary__(data)
            else:
                subsection.set(item, data)
        elif isinstance(data, dict):
            subsection = self.__get_or_create_subsection__(section, parent=self)
            subsection.__load_dictionary__(data)
        else:
            raise ConfigurationError('not a dict')

    def __load_dictionary__(self, data):
        """
        Load settings from dictionary

        Any dictionaries in data are loaded as child configuration sections
        """
        if not isinstance(data, dict):
            raise ConfigurationError(f'Dictionary is not dict instance: {data}')

        for key, value in data.items():
            attr, path = self.__split_attribute_path__(key)
            if path:
                self.__load_section__(attr, value, path)
            elif isinstance(value, dict):
                self.__load_section__(attr, value)
            else:
                self.set(key, value)

    def as_dict(self):
        """
        Return configuration section as dictionary
        """
        data = super().as_dict()
        for subsection in self.__subsections__:
            data[subsection.__name__] = subsection.as_dict()
        return data

    def set(self, attr, value):
        """
        Set configuration setting value as attribute of the object

        Attributes are set as ConfigurationItem classes by default.
        """
        attr, path = self.__split_attribute_path__(attr)
        if path:
            self.__load_section__(attr, value, path)
            return

        self.__validate_attribute__(attr)
        super().set(attr, value)

    def validate(self):
        """
        Validate loaded configuration settings

        Default implementation checks if required settings are set.
        """
        for attr in self.__required_settings__:
            value = getattr(self, attr, None)
            if value is None:
                raise ConfigurationError(f'{self} required setting {attr} has no value')


class ConfigurationFile(ConfigurationSection):
    """
    Common base class for configuration file parsers
    """
    __default_paths__ = []

    def __init__(self, path=None, parent=None, debug_enabled=False, silent=False):
        self.__path__ = Path(path).expanduser() if path is not None else None
        super().__init__(parent=parent, debug_enabled=debug_enabled, silent=silent)

        # Load any common default paths
        for default_path in self.__default_paths__:
            default_path = Path(default_path)
            if default_path.is_file():
                self.load(default_path)

        # Load specified configuration file
        if self.__path__ is not None and self.__path__.exists():
            self.load(self.__path__)

    def __repr__(self):
        return str(self.__path__.name) if self.__path__ is not None else ''

    @staticmethod
    def __check_file_access__(path):
        """
        Check access to specified path as file

        Raises ConfigurationError if path is not a file or not readable
        """
        path = Path(path).expanduser()
        if not path.is_file():
            raise ConfigurationError(f'No such file: {path}')
        if not os.access(path, os.R_OK):
            raise ConfigurationError(f'Permission denied: {path}')
        return path

    def load(self, path):
        """
        Load specified configuration file

        This method must be implemted in child class
        """
        raise NotImplementedError('File loading must be implemented in child class')

    def parse_data(self, data):
        """
        Parse data read from configuration file

        Default implementation requires data is a dictionary
        """
        if data is None:
            return
        if not isinstance(data, dict):
            raise ConfigurationError(f'Data is not dict instance: {data}')
        self.__load_dictionary__(data)


class IniConfiguration(ConfigurationFile):
    """
    Configuration parser for INI style configuration files

    You can pass arguments to configparser.ConfigParser with
    loader_args
    """
    def __init__(self, path=None, parent=None, debug_enabled=False, silent=False, **loader_args):
        self.__loader_args__ = loader_args
        super().__init__(path, parent=parent, debug_enabled=debug_enabled, silent=silent)

    def load(self, path):
        """
        Load specified INI configuration file
        """
        path = self.__check_file_access__(path)
        parser = configparser.ConfigParser(**self.__loader_args__)
        try:
            parser.read(path)
        except Exception as error:
            raise ConfigurationError(f'Error loading {path}: {error}') from error

        for section_name in parser.sections():
            self.__load_section__(
                section_name,
                dict(parser[section_name].items())
            )


class JsonConfiguration(ConfigurationFile):
    """
    Configuration parser for JSON configuration files

    You can pass arguments to json.loads with loader_args
    """
    encoding = 'utf-8'

    def __init__(self, path=None, parent=None, debug_enabled=False, silent=False, **loader_args):
        self.__loader_args__ = loader_args
        super().__init__(path, parent=parent, debug_enabled=debug_enabled, silent=silent)

    def load(self, path):
        """
        Load specified JSON configuration file
        """
        path = self.__check_file_access__(path)
        try:
            self.parse_data(
                json.loads(path.open('r', encoding=self.encoding).read(), **self.__loader_args__)
            )
        except Exception as error:
            raise ConfigurationError(f'Error loading {path}: {error}') from error


class YamlConfiguration(ConfigurationFile):
    """
    Configuration parser for yaml configuration files
    """
    encoding = 'utf-8'

    def load(self, path):
        """
        Load specified YAML configuration file
        """
        path = self.__check_file_access__(path)

        try:
            self.parse_data(
                yaml.safe_load(path.open('r', encoding='utf-8'))
            )
        except Exception as error:
            raise ConfigurationError(f'Error loading {path}: {error}') from error
