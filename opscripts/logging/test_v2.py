# vim: set fileencoding=utf-8 :

"""Unit Tests
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import logging
import os.path
import sys

# Third-party
import pytest

# Local/library specific
from . import v2 as ops_logging


@pytest.fixture(scope="function")
def opslog(request):
    log_level = logging.getLogger().getEffectiveLevel()
    prog = os.path.basename(sys.argv[0])
    opslog = ops_logging.OpScriptsLogging(prog)

    def teardown():
        opslog.logger.removeHandler(opslog.handler_screen)
        opslog.logger.removeHandler(opslog.handler_syslog)
        opslog.logger.setLevel(log_level)

    request.addfinalizer(teardown)

    return opslog


def test_logger_instance_creation(opslog):
    # GIVEN ops_logging initialization
    # WHEN nothine else is done
    # THEN there should be no filters and
    #      there should be three handlers and
    #      the screen handler should be present and
    #      the syslog handler should be present and
    #      the log level should be 30 WARNING
    assert len(opslog.logger.filters) == 0
    assert len(opslog.logger.handlers) == 2
    assert opslog.handler_screen in opslog.logger.handlers
    assert opslog.handler_syslog in opslog.logger.handlers
    assert opslog.logger.getEffectiveLevel() == logging.WARNING


def test_dryrun(opslog):
    # GIVEN ops_logging initialization
    # WHEN dryrun function is invoked with True
    opslog.dryrun(True)
    # THEN there should be one handler and
    #      the screen handler should be present
    assert len(opslog.logger.handlers) == 1
    assert opslog.logger.handlers[0] == opslog.handler_screen


def test_set_log_level__num_log_level_above_max(opslog):
    # GIVEN ops_logging initialization
    # WHEN set_log_level function is invoked with a verbosity total well above
    #      the maximum allowed by the function (50 CRITICAL)
    ten_quiet_flags = [10] * 10
    opslog.set_log_level(ten_quiet_flags)
    # THEN the log level should be CRITICAL
    assert opslog.logger.getEffectiveLevel() == logging.CRITICAL


def test_set_log_level__num_log_level_below_min(opslog):
    # GIVEN ops_logging initialization
    # WHEN set_log_level function is invoked with a verbosity total well below
    #      the minimum allowed by the function (10 DEBUG)
    ten_verbose_flags = [-10] * 10
    opslog.set_log_level(ten_verbose_flags)
    # THEN the log level should be DEBUG
    assert opslog.logger.getEffectiveLevel() == logging.DEBUG


def test_remove_syslog_handler(opslog):
    # GIVEN ops_logging initialization
    # WHEN remove_syslog_handler function is invoked
    opslog.remove_syslog_handler()
    # THEN there should be one handler and
    #      the screen handler should be present
    assert len(opslog.logger.handlers) == 1
    assert opslog.logger.handlers[0] == opslog.handler_screen
