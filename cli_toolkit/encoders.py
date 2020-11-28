"""
Encoders for data
"""

import json
import yaml

from datetime import datetime, date, time, timedelta

import pytz


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
            obj = obj.astimezone(pytz.UTC)

        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()

        if isinstance(obj, timedelta):
            return (datetime.min + obj).time().isoformat()

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
