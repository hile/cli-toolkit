"""
Encoders for data
"""

import json

from datetime import datetime, date, time, timedelta, timezone

import yaml


def format_timedelta(value, with_prefix=True):
    """
    Format python datetime timedelta value as ISO format time string
    (HH:MM:SS.MS) with +- prefix.

    Value can either be datetime.timedelta instance or float string representing total seconds in
    timedelta

    If value is negative and with_prefix is False, raise ValueError because such timestamp can't be
    presented correctly without prefix
    """
    if isinstance(value, timedelta):
        value = value.total_seconds()
    if not isinstance(value, float):
        try:
            value = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError('format_timedelta() value must be a timedelta or float') from error

    if value < 0 and not with_prefix:
        raise ValueError('format_timedelta() negative timedelta requires with_prefix=True')
    negative = value < 0
    value = (datetime.min + timedelta(seconds=abs(value))).time().isoformat()

    if with_prefix:
        prefix = '+' if not negative else '-'
        return f'{prefix}{value}'
    return value


class DateTimeEncoder(json.JSONEncoder):
    """
    JSON encoder with datetime formatting as UTC
    """

    # pylint: disable=arguments-differ,method-hidden
    def default(self, obj):
        """
        Encode datetime, date and time as UTC
        """
        if isinstance(obj, datetime):
            obj = obj.astimezone(timezone.utc)

        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()

        if isinstance(obj, timedelta):
            return format_timedelta(obj, with_prefix=False)

        return super().default(obj)


def yaml_dump(data):
    """
    Call yaml.dump with dumper enforcing indentation and with explicit start
    marker in data

    This function generates yaml output that is compatible with yamlllint
    """
    class YamlDataDumper(yaml.Dumper):
        """
        Yaml data dumper implementation with parameters overridden for
        forced indentation
        """
        def increase_indent(self, flow=False, indentless=False):
            """
            AIgnore 'indentless' flag and always indent dumped data
            """
            return super().increase_indent(flow, False)

    return yaml.dump(
        data,
        Dumper=YamlDataDumper,
        default_flow_style=False,
        explicit_start=True,
        explicit_end=False
    )
