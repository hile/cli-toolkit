"""
Utilities for operating system platform detection

Platform detection uses sys.platform to detect platform family
(darwin, linux, bsd, openbsd) and platform toolchain family
(gnu, bsd, openbsd)
"""

import sys
import re

# Group OS by platform
PLATFORM_PATTERNS = {
    'darwin': {
        r'^darwin$',
    },
    'linux': (
        r'^linux$',
        r'^linux\d+$',
    ),
    'bsd': (
        r'^freebsd$',
        r'^freebsd\d+$',
    ),
    'openbsd': {
        r'^openbsd$',
        r'^openbsd\d+$',
    }
}

# Group OS by primary toolchain platform
TOOLCHAIN_FAMILY_PATTERNS = {
    'gnu': (
        r'^linux$',
        r'^linux\d+$',
    ),
    'bsd': (
        r'^darwin$',
        r'^freebsd$',
        r'^freebsd\d+$',
    ),
    'openbsd': (
        r'^openbsd$',
        r'^openbsd\d+$',
    )
}


def detect_platform_family():
    """
    Detect OS platform family from sys.platform, grouping similar operating systems to single
    label based on PLATFORM_PATTERNS
    """
    for family, patterns in PLATFORM_PATTERNS.items():
        for pattern in patterns:
            if pattern == sys.platform or re.compile(pattern).match(sys.platform):
                return family
    raise ValueError(f'Error detecting OS platform family from {sys.platform}')


def detect_toolchain_family():
    """
    Detect CLI toolchain family from sys.platform, grouping similar operating system to singel
    label based on TOOLCHAIN_FAMILY_PATTERNS
    """
    for family, patterns in TOOLCHAIN_FAMILY_PATTERNS.items():
        for pattern in patterns:
            if pattern == sys.platform or re.compile(pattern).match(sys.platform):
                return family
    raise ValueError(f'Error detecting CLI toolchain family from {sys.platform}')
