"""
Unit tests for cli_toolkit.path.Executables class
"""

import os

from pathlib import Path

from cli_toolkit.path import Executables


def test_path_executables_load():
    """
    Test loading instance of path executables object
    """
    executables = Executables()
    assert isinstance(executables.__repr__(), str)
    assert executables.__repr__() == os.environ['PATH']

    assert len(executables) > 0
    assert 'sh' in executables
    assert isinstance(executables['sh'], Path)
    assert list(executables) != []

    other = Executables()
    assert len(executables) == len(other)

    assert executables.get('jvodsav') is None
    assert isinstance(executables.get('sh'), Path)

    paths = executables.paths('sh')
    assert len(paths) == 1
    for path in paths:
        assert isinstance(path, Path)
