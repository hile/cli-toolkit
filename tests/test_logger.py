
import logging
import sys

from pathlib import Path

import pytest

from cli_toolkit.logger import (
    get_default_syslog_address,
    Logger,
    LoggerError,
    DEFAULT_TARGET_NAME
)

DEFAULT_LOG_LEVEL = logging.WARN


def test_logger_defaults():
    """
    Test initializing default logger
    """
    logger = Logger()
    assert logger.level == DEFAULT_LOG_LEVEL

    # pylint: disable=no-member
    default = logger.default

    assert logger.__repr__() == DEFAULT_TARGET_NAME
    assert default is not None
    assert default.level == logger.level


def test_logger_default_set_level():
    """
    Test setting default logger level
    """
    logger = Logger()
    assert logger.level == DEFAULT_LOG_LEVEL

    # pylint: disable=no-member
    default = logger.default
    assert default.level == logger.level

    logger.level = logging.DEBUG
    assert default.level == logging.DEBUG

    logger.level = DEFAULT_LOG_LEVEL
    logger.level = 'DEBUG'
    assert default.level == logging.DEBUG

    with pytest.raises(LoggerError):
        logger.level = 'NILITYS'

    # Return to default, the object persists between test cases
    logger.level = DEFAULT_LOG_LEVEL


def test_logger_multiple_init():
    """
    Test initializing default logger more than once, returning
    same logger instances
    """
    logger = Logger()
    assert logger.level == DEFAULT_LOG_LEVEL

    # pylint: disable=no-member
    default = logger.default

    assert default is not None
    assert default.level == logger.level

    # pylint: disable=no-member
    other = Logger().default
    assert other.__hash__ == default.__hash__

    # This is different logger group
    # pylint: disable=no-member
    different = Logger('test').default
    assert different.__hash__ == default.__hash__


def test_logger_register_stream_handler():
    """
    Test registering additional stream handler to logger
    """
    logger = Logger()
    logger.register_stream_handler('test')
    logger.register_stream_handler('test')
    logger.register_stream_handler('testing')

    # pylint: disable=no-member
    default = logger.default
    # pylint: disable=no-member
    test = logger.test
    # pylint: disable=no-member
    testing = logger.testing

    assert test is not None
    assert testing is not None

    assert default != test
    assert test != testing


def test_logger_register_syslog_handler():
    """
    Test registering additional syslog handler to logger
    """
    logger = Logger()
    logger.register_syslog_handler('test')
    logger.register_syslog_handler('testing')

    logger.register_syslog_handler('test', address='127.0.0.1')

    # pylint: disable=no-member
    default = logger.default
    # pylint: disable=no-member
    test = logger.test
    # pylint: disable=no-member
    testing = logger.testing

    assert test is not None
    assert testing is not None

    assert default != test
    assert test != testing

    reregister = logger.register_syslog_handler('test')
    assert reregister is not None
    assert test.__hash__() == reregister.__hash__()


def test_logger_register_http_handler():
    """
    Test registering additional HTTP handler to logger
    """

    url = 'http://example.com'
    other_url = 'http://localhost:8000/'
    logger = Logger()
    logger.register_http_handler('test', url)
    logger.register_http_handler('test', other_url)

    # pylint: disable=no-member
    default = logger.default
    # pylint: disable=no-member
    test = logger.test
    # pylint: disable=no-member
    testing = logger.testing

    assert test is not None
    assert testing is not None

    assert default != test
    assert test != testing

    reregister = logger.register_http_handler('test', url)
    assert reregister is not None
    assert test.__hash__() == reregister.__hash__()


def test_logger_register_file_handler(tmpdir):
    """
    Test registering additional file handler to logger
    """

    logger = Logger()
    logger.register_file_handler('test', tmpdir)
    assert Path(tmpdir).joinpath('test.log').is_file()

    logger.register_file_handler('test', tmpdir)
    assert Path(tmpdir).joinpath('test.log').is_file()

    logger.register_file_handler('test', tmpdir, filename='test-other.log')
    assert Path(tmpdir).joinpath('test-other.log').is_file()

    logger.register_file_handler('testing', tmpdir, filename='tester-log')
    assert Path(tmpdir).joinpath('tester-log').is_file()

    subdir = Path(tmpdir, 'sub')
    logger.register_file_handler('test-sub', subdir)
    assert Path(subdir, 'test-sub.log').is_file()

    # pylint: disable=no-member
    default = logger.default
    # pylint: disable=no-member
    test = logger.test
    # pylint: disable=no-member
    testing = logger.testing

    assert test is not None
    assert testing is not None

    assert default != test
    assert test != testing

    reregister = logger.register_file_handler('test', tmpdir)
    assert reregister is not None
    assert test.__hash__() == reregister.__hash__()


def test_logger_register_syslog_handler_invalid_level():
    """
    Test registering additional HTTP handler to logger with invalid URL
    """
    logger = Logger()
    with pytest.raises(LoggerError):
        logger.register_syslog_handler('test', default_level='pimpelipom')


def test_logger_register_http_handler_invalid_url():
    """
    Test registering additional HTTP handler to logger with invalid URL
    """

    url = ''
    logger = Logger()
    with pytest.raises(LoggerError):
        logger.register_http_handler('test', url)


# pylint: disable=unused-argument
def test_logger_register_fil_handler_os_error(mock_path_mkdir_permission_denied, mock_permission_denied):
    """
    Test registering additional HTTP handler to logger with invalid URL
    """
    logger = Logger()
    with pytest.raises(LoggerError):
        logger.register_file_handler('test', '/92977BB4-C1A5-4E6D-A731-1E4BF2328ACC')


def test_logger_mock_platform_darwin(monkeypatch):
    """
    Test mocked logger loading with darwin platform
    """
    monkeypatch.setattr(sys, 'platform', 'darwin')
    assert sys.platform == 'darwin'
    assert isinstance(get_default_syslog_address(), str)


def test_logger_mock_platform_linux(monkeypatch):
    """
    Test mocked logger loading with linux platform
    """
    monkeypatch.setattr(sys, 'platform', 'linux')
    assert sys.platform == 'linux'
    assert isinstance(get_default_syslog_address(), str)


def test_logger_mock_platform_freebsd(monkeypatch):
    """
    Test mocked logger loading with freebsd platform
    """
    monkeypatch.setattr(sys, 'platform', 'freebsd12')
    assert sys.platform == 'freebsd12'
    assert isinstance(get_default_syslog_address(), str)


def test_logger_mock_platform_windows(monkeypatch):
    """
    Test mocked logger loading with windows platform
    """
    monkeypatch.setattr(sys, 'platform', 'windows')
    assert sys.platform == 'windows'
    assert isinstance(get_default_syslog_address(), tuple)
