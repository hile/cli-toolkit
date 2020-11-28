"""
Example CLI utility confifguration parser for cli-toolkit
"""

from cli_toolkit.configuration import YamlConfiguration

# Configuration classes expand ~ and $HOME
DEFAULT_SYSTEM_PATH = '/etc/defaults/cli_demo.yml'
DEFAULT_PATH = '~/.config/cli_demo.yml'


class Configuration(YamlConfiguration):
    """
    Example yaml configuration file parser for demos
    """
    __default_paths__ = (
        DEFAULT_SYSTEM_PATH,
        DEFAULT_PATH
    )
    """
    Optional configuration files to load
    """
