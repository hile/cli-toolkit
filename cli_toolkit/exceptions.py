"""
Exceptions raised by cli-toolkit
"""


class ConfigurationError(Exception):
    """
    Errors raised by configuration processing
    """


class FileParserError(Exception):
    """
    Exceptions raised while parsing text files
    """


class LoggerError(Exception):
    """
    Exceptions raised by logging configuration
    """


class ScriptError(Exception):
    """
    Errors raise during script processing
    """
