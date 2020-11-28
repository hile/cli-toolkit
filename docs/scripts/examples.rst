
CLI script examples
###################

This page contains examples for using script and command classes.

Minimal example script example without using subcommands:

.. literalinclude:: ../examples/simple_script.py

Example output:

.. code-block:: text

    # python3 docs/source/examples/simple_script.py -t 'test debug message'
    # python3 docs/source/examples/simple_script.py --debug -t 'test debug message'
    test debug message


Minimal demo of using script subcommands:

.. literalinclude:: ../examples/simple_script_subcommand.py

Output from the example command with various arguments:

.. code-block:: text

    # python3 docs/source/examples/simple_script_subcommand.py
    No command selected
    # python3 docs/source/examples/simple_script_subcommand.py demo
    No tag specified
    # python3 docs/source/examples/simple_script_subcommand.py demo -t 'test tag'
    test tag
