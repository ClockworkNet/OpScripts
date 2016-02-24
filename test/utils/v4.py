# vim: set fileencoding=utf-8 :

"""Unit Tests
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import logging

# Third-party
import pytest

# Local/library specific
from opscripts.utils import v4 as ops_utils


DOC = """\
Alfa        Bravo    Charlie
----        -----    -------
apple           1          x
banana         22  xxxxxxxxx
Clementine    333         xx\
"""


def test_format_columns():
    # GIVEN a preformatted DOC and the following rows list of lists
    rows = [["Alfa", "Bravo", "Charlie"],
            ["----", "-----", "-------"],
            ["apple", 1, "x"],
            ["banana", 22, "xxxxxxxxx"],
            ["Clementine", 333, "xx"]]
    # WHEN rows is formatted and joined into a single string
    result = "\n".join(ops_utils.format_columns(rows, ["<", ">", ">"]))
    # THEN the result of format_columns should match preformatted DOC
    assert result == DOC


def test_log_ctrlc_and_exit(capfd, caplog):
    # GIVEN opslog invocation
    # WHEN the ops_utils.log_ctrlc_and_exit function is invoked and
    #      the output is captured
    with pytest.raises(SystemExit) as e:
        ops_utils.log_ctrlc_and_exit()
    out, err = capfd.readouterr()
    # THEN a SystemExit exception should be raised and
    #      the exit status should be 130 and
    #      there should be only a single newline written to stderr and
    #      there should be a single log message and
    #      the log level of the message should be INFO and
    #      the log message should match the expected text
    assert int(str(e.value)) == 130
    assert err == "\n"
    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.INFO
    assert caplog.records[0].message == "(130) Halted via KeyboardInterrupt."


def test_log_ctrlc_and_exit__without_logging(capfd):
    # GIVEN the caplog logging handler is removed and
    #       the expected output to stderr
    root_logger = logging.getLogger()
    handler = root_logger.handlers[0]
    root_logger.removeHandler(handler)
    tested = __name__.split(".")
    tested = ".".join([tested[0], tested[1], tested[2].split("_")[1]])
    expected_err = ("\nCRITICAL No handlers could be found for logger \"{0}\""
                    "\nINFO (130) Halted via KeyboardInterrupt.\n"
                    .format(tested))
    # WHEN the ops_utils.log_ctrlc_and_exit function is invoked and
    #      the output is captured
    with pytest.raises(SystemExit) as e:
        ops_utils.log_ctrlc_and_exit()
    out, err = capfd.readouterr()
    # THEN a SystemExit exception should be raised and
    #      the exit status should be 130 and
    #      stderr should match the expected error message
    assert int(str(e.value)) == 130
    assert err == expected_err


def test_log_exception(capfd, caplog):
    # GIVEN the expected output to logging
    expected_log_start = "(1) Fatal: (4) test_log_exception:"
    eel = len(expected_log_start)
    # WHEN a ops_utils.Fatal is raised and
    #      the exception is logged via ops_utils.log_exception and
    #      the output is captured
    try:
        raise ops_utils.Fatal("test_log_exception", 4)
    except:
        ops_utils.log_exception()
    out, err = capfd.readouterr()
    # THEN there should be nothing written to stderr and
    #      there should be a single log message and
    #      the log level of the message should be CRITICAL and
    #      the beginning of log message should match the expected text
    assert err == ""
    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.CRITICAL
    assert caplog.records[0].message[0:eel] == expected_log_start


def test_log_exception_and_exit(capfd, caplog):
    # GIVEN the expected output to logging
    expected_log_start = "(1) Fatal: (3) test_log_exception_and_exit:"
    eel = len(expected_log_start)
    # WHEN a ops_utils.Fatal is raised and
    #      the exception is logged via ops_utils.log_exception_and_exit and
    #      the output is captured
    with pytest.raises(SystemExit) as e:
        try:
            raise ops_utils.Fatal("test_log_exception_and_exit", 3)
        except:
            ops_utils.log_exception_and_exit()
    out, err = capfd.readouterr()
    # THEN a SystemExit exception should be raised and
    #      the exit status should be 2 and
    #      there should be nothing written to stderr and
    #      there should be a single log message and
    #      the log level of the message should be CRITICAL and
    #      the beginning of log message should match the expected text
    assert int(str(e.value)) == 1
    assert err == ""
    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.CRITICAL
    assert caplog.records[0].message[0:eel] == expected_log_start


def test_log_fatal_and_exit(capfd, caplog):
    # GIVEN the expected output to logging
    expected_log = "(2) test_log_fatal_and_exit"
    # WHEN a ops_utils.Fatal is raised and
    #      the output is captured
    with pytest.raises(SystemExit) as e:
        try:
            raise ops_utils.Fatal("test_log_fatal_and_exit", 2)
        except:
            ops_utils.log_fatal_and_exit()
    out, err = capfd.readouterr()
    # THEN a SystemExit exception should be raised and
    #      the exit status should be 2 and
    #      there should be nothing written to stderr and
    #      there should be a single log message and
    #      the log level of the message should be CRITICAL and
    #      the beginning of log message should match the expected text
    assert int(str(e.value)) == 2
    assert err == ""
    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == logging.CRITICAL
    assert caplog.records[0].message == expected_log


def test_verify_root(capfd):
    # GIVEN the expected error message
    expected_err = ("(77) Must be root or equivalent (ex. sudo).")
    # WHEN ops_utils.verify_root() is invoked as a non-root user
    with pytest.raises(ops_utils.Fatal) as e:
        ops_utils.verify_root()
    out, err = capfd.readouterr()
    # THEN the exception message should match the expected error message
    assert str(e.value) == expected_err
