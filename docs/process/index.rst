Processes
#########

Process module contains wrappers for running shell commands. The wrappers are
implemented with subprocess.Pope

run_command
===========

Runs specified command silently with stdin, stdout and stderr set to PIPE, checks
return code matches expected values and raises ScriptError if not. Returns raw
stdout and stderr outputs as bytes.

run_command_lineoutput
======================

Run specified shell command with run_command, split stdout and stderr to lines and
encode the lines as utf-8 strings.

.. toctree::
    :maxdepth: 1
