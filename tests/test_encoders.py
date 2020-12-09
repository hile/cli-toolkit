"""
Test cli_toolkit.encoders functions
"""

import json

from datetime import datetime, timedelta

import pytz
import pytest

from cli_toolkit.encoders import DateTimeEncoder, format_timedelta, yaml_dump

TEST_DATE = datetime(
    year=2020, month=1, day=2, hour=1, minute=2, second=3,
    tzinfo=pytz.UTC
)

TEST_DICT = {
    'a': 1,
    'b': [1, 2, 3]
}
YAML_DUMP_RESULT = """---
a: 1
b:
  - 1
  - 2
  - 3
"""

TIMEDELTA_VALID = (
    {
        'values': ['0', 0, 0.0, timedelta(seconds=0)],
        'output': '+00:00:00',
    },
)
TIMEDELTA_INVALID = (
    None,
    [],
    'invalid'
)


def test_encoders_error():
    """
    Test encoding value which is not supported
    """
    testdata = {'string': b'string value'}
    with pytest.raises(TypeError):
        json.dumps(testdata, cls=DateTimeEncoder)


def test_format_timedelta_valid():
    """
    Test format_timedelta with various valid values
    """
    for testcase in TIMEDELTA_VALID:
        for value in testcase['values']:
            prefixed = testcase['output']
            noprefix = testcase['output'].lstrip('+-')
            assert format_timedelta(value) == prefixed
            assert format_timedelta(value, with_prefix=False) == noprefix


def test_format_timedelta_negative():
    """
    Test parsing negative time delta values
    """
    testcase = timedelta(seconds=-3623)
    expected = '-01:00:23'
    with pytest.raises(ValueError):
        format_timedelta(testcase, with_prefix=False)
    assert format_timedelta(testcase) == expected


def test_format_timedelta_errors():
    """
    Test format_timedelta with various invalid values
    """
    for testcase in TIMEDELTA_VALID:
        with pytest.raises(ValueError):
            format_timedelta(testcase)


# pylint: disable=unused-argument
def test_encoders_datetime_naive():
    """
    Test encoding naive datetime
    """
    testdata = {'datetime': TEST_DATE}
    expected = f'{{"datetime": "{TEST_DATE.isoformat()}"}}'
    value = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(value, str)
    assert value == expected


def test_encoders_datetime_with_timezone():
    """
    Test encoding datetime with different timezone values
    """
    testdata = {'datetime': TEST_DATE.astimezone(pytz.timezone('Europe/Helsinki'))}
    expected = f'{{"datetime": "{TEST_DATE.isoformat()}"}}'
    result = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(result, str)
    assert result == expected

    testdata = {'datetime': TEST_DATE.astimezone(pytz.timezone('US/Eastern'))}
    result = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(result, str)
    assert result == expected


def test_encoders_datetime_date():
    """
    Test encoding date value
    """
    testdata = {'date': TEST_DATE.date()}
    value = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(value, str)
    assert value == '{"date": "2020-01-02"}'


def test_encoders_datetime_time():
    """
    Test encoding time value
    """
    testdata = {'time': TEST_DATE.time()}
    value = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(value, str)
    assert value == '{"time": "01:02:03"}'


def test_encoders_datetime_timedelta():
    """
    Test encoding timedelta
    """
    testdata = {'delta': timedelta(hours=10)}
    value = json.dumps(testdata, cls=DateTimeEncoder)
    assert isinstance(value, str)
    assert value == '{"delta": "10:00:00"}'


def test_encoders_yaml_dump():
    """
    Test yaml_dump method returns expected document
    """
    assert yaml_dump(TEST_DICT) == YAML_DUMP_RESULT
