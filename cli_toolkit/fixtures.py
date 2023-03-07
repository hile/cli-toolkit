#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Shared fixtures for unit tests
"""
import sys
from typing import List, Iterator

import pytest


@pytest.fixture
def cli_mock_argv(monkeypatch) -> Iterator[List[str]]:
    """
    Fixture to set argv for argparse tests
    """
    arguments = ['test-cli']
    monkeypatch.setattr(sys, 'argv', arguments)
    yield arguments
