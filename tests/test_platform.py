
import sys

import pytest

from cli_toolkit.platform import (
    detect_platform_family,
    detect_toolchain_family
)

PLATFORM_TESTS = (
    ('darwin', 'darwin'),
    ('freebsd9', 'bsd'),
    ('freebsd12', 'bsd'),
    ('linux', 'linux'),
    ('linux2', 'linux'),
    ('openbsd6', 'openbsd'),
    ('openbsd', 'openbsd'),
)
TOOLCHAIN_TESTS = (
    ('darwin', 'bsd'),
    ('freebsd9', 'bsd'),
    ('freebsd12', 'bsd'),
    ('linux', 'gnu'),
    ('linux2', 'gnu'),
    ('openbsd6', 'openbsd'),
    ('openbsd', 'openbsd'),
)


def test_unsupported_platform_family(monkeypatch):
    """
    Test detection of OS families with invalid platform
    """
    monkeypatch.setattr(sys, 'platform', 'nothing_os')
    with pytest.raises(ValueError):
        detect_platform_family()


def test_unsupported_platform_toolchain(monkeypatch):
    """
    Test detection of OS toolchain with invalid platform
    """
    monkeypatch.setattr(sys, 'platform', 'nothing_os')
    with pytest.raises(ValueError):
        detect_toolchain_family()


def test_platform_family_detection(monkeypatch):
    """
    Test detection of OS families from sys.platform strings
    """
    for test in PLATFORM_TESTS:
        mock_platform = test[0]
        expected_family = test[1]
        monkeypatch.setattr(sys, 'platform', mock_platform)
        assert expected_family == detect_platform_family()


def test_platform_toolchain_detection(monkeypatch):
    """
    Test detection of OS toolchains from sys.platform strings
    """
    for test in TOOLCHAIN_TESTS:
        mock_platform = test[0]
        expected_toolchain = test[1]
        monkeypatch.setattr(sys, 'platform', mock_platform)
        assert expected_toolchain == detect_toolchain_family()
