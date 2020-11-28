Logging
#######

Logger is a wrapper for more userfriendly python logging.

Logging module extends standard python logging by providing a singleton instance
of logging targets grouped by name. Multiple log targets can be registered to
each group and the module prevents initializing same logging target twice.

Logger also sets some reasonable log output and time formats by default.

Log levels for all log targets in a group are synchronized and can be set either
by logging module constants (logging.DEBUG) or by string names ('DEBUG')

If no name is specified, group `default` is initialized.

.. code-block:: python

    from cli_toolkit.logger import Logger

    logger = Logger()
    logger.level = 'DEBUG'
    log = logger.default
    log.debug('test message')

    other = Logger('tests')
    test_log = other.tests
    test_log.debug('no message')

    Logger().default.debug('another test message')

Previous example opens default logging

.. toctree::
    :maxdepth: 1

    default
    file
    http
    syslog
