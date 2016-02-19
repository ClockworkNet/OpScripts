# vim: set fileencoding=utf-8 :

"""Test for OpScripts logging library
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import logging
import os.path
import sys

# Third-party
from nose.tools import with_setup

# Local/library specific
from . import v2 as ops_logging


LOG_LEVEL = None
LOGGER = None


def setup_module(module):
    global LOG_LEVEL
    LOG_LEVEL = logging.getLogger().getEffectiveLevel()


def teardown_module(module):
    pass


def setup_function():
    global LOGGER
    prog = os.path.basename(sys.argv[0])
    LOGGER = ops_logging.OpScriptsLogging(prog)


def teardown_function():
    global LOGGER
    LOGGER.logger.removeHandler(LOGGER.handler_screen)
    LOGGER.logger.removeHandler(LOGGER.handler_syslog)
    LOGGER.logger.setLevel(LOG_LEVEL)
    del LOGGER


@with_setup(setup_function, teardown_function)
def test_handler_creation():
    # GIVEN ops_logging initialization
    # WHEN nothine else is done
    # THEN there should be three handlers (nose, screen, and syslog) and
    #      the log level should be WARNING
    assert (len(LOGGER.logger.handlers) == 3 and
            LOGGER.logger.getEffectiveLevel() == logging.WARNING)


@with_setup(setup_function, teardown_function)
def test_dryrun():
    # GIVEN ops_logging initialization
    # WHEN dryrun function is invoked with True
    LOGGER.dryrun(True)
    # THEN there should be two handlers (nose and screeng)
    assert len(LOGGER.logger.handlers) == 2


@with_setup(setup_function, teardown_function)
def test_set_log_level_too_quiet():
    # GIVEN ops_logging initialization
    # WHEN set_log_level function is invoked with a verbosity well above the
    #      maximum
    LOGGER.set_log_level([100])
    # THEN the log level should be CRITICAL
    assert LOGGER.logger.getEffectiveLevel() == logging.CRITICAL


@with_setup(setup_function, teardown_function)
def test_set_log_level_too_verbose():
    # GIVEN ops_logging initialization
    # WHEN set_log_level function is invoked with a verbosity well below the
    #      minimum
    LOGGER.set_log_level([-100])
    # THEN the log level should be DEBUG
    assert LOGGER.logger.getEffectiveLevel() == logging.DEBUG


@with_setup(setup_function, teardown_function)
def test_remove_syslog_handler():
    # GIVEN ops_logging initialization
    # WHEN remove_syslog_handler function is invoked
    LOGGER.remove_syslog_handler()
    # THEN there should be two handlers (nose and screeng)
    assert len(LOGGER.logger.handlers) == 2
