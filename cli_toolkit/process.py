"""
Execute shell commands and return output

Wraps subprocess.run, linking error handling to ScriptError and handling
common string output use cases.
"""

import os

from subprocess import run, PIPE, CalledProcessError, TimeoutExpired

from .exceptions import ScriptError

DEFAULT_ENCODINGS = (
    'utf-8',
)
DEFAULT_RETURN_CODES_OK = [0]


def run_command(*args, cwd=None, expected_return_codes=None, env=None, timeout=None):
    """
    Run command as subprocess, checking return code is 0 and returning stdout
    and stderr as bytes

    Optional timeout value can be set to cause command to abort after specified timeout
    """
    if env is None:
        env = os.environ.copy()
    if expected_return_codes is None:
        expected_return_codes = DEFAULT_RETURN_CODES_OK

    try:
        # pylint: disable=subprocess-run-check
        res = run(args, stdout=PIPE, stderr=PIPE, check=False, cwd=cwd, env=env, timeout=timeout)
        if res.returncode not in expected_return_codes:
            raise ScriptError(
                f'Error running {" ".join(args)}: returns {res.returncode}: {res.stderr}'
            )
    except (CalledProcessError, FileNotFoundError, TimeoutExpired) as error:
        raise ScriptError(error) from error

    return res.stdout, res.stderr


def run_command_lineoutput(*args, cwd=None, expected_return_codes=None, env=None,
                           timeout=None, encodings=DEFAULT_ENCODINGS):
    """
    Run command as subprocess, checking return code is 0 and returning stdout and
    stderr as split to lines

    Each line is as string with specified encodings. A file can contain multiple
    encodings, i.e. mixed UTF-8 and latin1 strings. When multiple encodings are
    detected the line is returned encoded with first suitable encoder
    """
    def parse_line(line, encodings):
        """
        Parse line from bytes to str with list of encodings
        """
        for encoding in encodings:
            try:
                return str(line, encoding)
            except ValueError:
                pass
        raise ScriptError(f'Error parsing line {line}')

    if expected_return_codes is None:
        expected_return_codes = DEFAULT_RETURN_CODES_OK
    stdout, stderr = run_command(
        *args,
        cwd=cwd,
        timeout=timeout,
        expected_return_codes=expected_return_codes,
        env=env
    )
    stdout = [parse_line(line, encodings) for line in stdout.splitlines()]
    stderr = [parse_line(line, encodings) for line in stderr.splitlines()]
    return stdout, stderr
