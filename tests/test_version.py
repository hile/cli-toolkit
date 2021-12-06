
from sys_toolkit.tests.packaging import validate_version_string

from cli_toolkit import __version__


def test_version_string():
    """
    Test format of module version string validation
    """
    validate_version_string(__version__)
