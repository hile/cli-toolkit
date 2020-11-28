"""
User PATH command lookup cache

>>> from cli_toolkit.path import Executables
>>> items = Executables()
>>> item['bash']
PosixPath('/bin/bash')
>>> item.get('bash')
PosixPath('/bin/bash')
>>> env.paths('python')
[PosixPath('/Users/hile/.venv/dev/bin/python'), PosixPath('/usr/bin/python')]
"""

import os

from collections.abc import Collection
from pathlib import Path


class Executables(Collection):
    """
    Singleton instance containing of executable commands on user's PATH

    Initializes a collections.abc.Collection lookup cache for commands on PATH

    Cache can be looked up by command name or with .get() method
    """
    __path__ = None
    """Path value being inspected"""
    __executables__ = []
    """List of all executables detected on path, including duplicate commands"""
    __commands__ = None
    """List of active commands on path"""

    def __init__(self):
        if Executables.__commands__ is None:
            Executables.__commands__ = Executables.__load__executables_on_path__(self)

    def __repr__(self):
        return self.__path__

    def __contains__(self, item):
        return item in self.__executables__ or item in self.__commands__

    def __iter__(self):
        return iter(self.__commands__.values())

    def __len__(self):
        return len(list(self.__commands__.keys()))

    def __getitem__(self, index):
        return self.__commands__[index]

    def __load__executables_on_path__(self):
        """
        Load executables available on user path
        """
        self.__executables__ = []
        commands = {}
        self.__path__ = os.environ.get('PATH', '')
        for path in self.__path__.split(os.pathsep):
            directory = Path(path)
            if not directory.is_dir():
                continue
            for filename in directory.iterdir():
                command = directory.joinpath(filename)
                try:
                    if not command.is_file() or not os.access(command, os.EX_OK):
                        continue
                except OSError:
                    pass
                self.__executables__.append(command)
                if filename.name not in commands:
                    commands[filename.name] = command
        return commands

    def paths(self, name):
        """
        Return all detected paths for command with specific name
        """
        return [
            item
            for item in self.__executables__
            if item.name == name
        ]

    def get(self, name):
        """
        Get path to command by name

        Return pathlib.Path reference to the command
        Returns None if command is not found
        """
        try:
            return self[name]
        except KeyError:
            return None
