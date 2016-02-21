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
from opscripts.logging import v2 as ops_logging
from opscripts.utils import v4 as ops_utils


DOC = """\
Alfa        Bravo    Charlie
----        -----    -------
apple           1          x
banana         22  xxxxxxxxx
Clementine    333         xx\
"""


@pytest.fixture(scope="function")
def opslog(request):
    log_level = logging.getLogger().getEffectiveLevel()
    prog = os.path.basename(sys.argv[0])
    opslog = ops_logging.OpScriptsLogging(prog)
    opslog.remove_syslog_handler()

    def teardown():
        opslog.logger.removeHandler(opslog.handler_screen)
        opslog.logger.setLevel(log_level)

    request.addfinalizer(teardown)

    return opslog


@pytest.fixture(scope="function")
def tested():
    tested = __name__.split(".")
    tested = ".".join([tested[0], tested[1], tested[2].split("_")[1]])
    return tested


def test_format_columns():
    # GIVEN a preformatted DOC and the following list of lists
    rows = [["Alfa", "Bravo", "Charlie"],
            ["----", "-----", "-------"],
            ["apple", 1, "x"],
            ["banana", 22, "xxxxxxxxx"],
            ["Clementine", 333, "xx"]]
    # WHEN rows is formatted and joined into a single string
    result = "\n".join(ops_utils.format_columns(rows, ["<", ">", ">"]))
    # THEN the result of format_columns should match preformatted DOC
    assert result == DOC


def test_log_ctrlc_and_exit__logging(capfd, opslog):
    # NOTE: I was unable to successfully capture stderr messages sent by
    #       logging. There *should* be more than a newline.
    #
    # GIVEN the expected output to stderr
    expected_err = "\n"
    # WHEN the ops_utils.log_ctrlc_and_exit function is invoked and
    #      the output is captured
    with pytest.raises(SystemExit) as e:
        ops_utils.log_ctrlc_and_exit()
    out, err = capfd.readouterr()
    # THEN a SystemExit exception should be raised and
    #      the exit status should be 130
    assert int(str(e.value)) == 130
    assert err == expected_err


def test_log_ctrlc_and_exit__print(capfd, tested):
    # GIVEN the expected output to stderr
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


def test_log_exception(capfd, tested):
    # GIVEN the expected output to stderr
    expected_err = ("CRITICAL No handlers could be found for logger \"{0}\""
                    "\nCRITICAL (1) Fatal: (2) test_log_fatal_and_exit:"
                    .format(tested))
    eel = len(expected_err)
    # WHEN a ops_utils.Fatal is raised and
    #      the exception is logged via ops_utils.log_exception and
    #      the output is captured
    try:
        raise ops_utils.Fatal("test_log_fatal_and_exit", 2)
    except:
        ops_utils.log_exception()
    out, err = capfd.readouterr()
    # THEN the beginning of stderr should match the expected error message
    assert err[0:eel] == expected_err


def test_log_exception_and_exit(capfd, tested):
    # GIVEN the expected output to stderr
    expected_err = ("CRITICAL No handlers could be found for logger \"{0}\""
                    "\nCRITICAL (1) Fatal: (2) test_log_exception_and_exit:"
                    .format(tested))
    eel = len(expected_err)
    # WHEN a ops_utils.Fatal is raised and
    #      the exception is logged via ops_utils.log_exception_and_exit and
    #      the output is captured
    with pytest.raises(SystemExit) as e:
        try:
            raise ops_utils.Fatal("test_log_exception_and_exit", 2)
        except:
            ops_utils.log_exception_and_exit()
    out, err = capfd.readouterr()
    # THEN a SystemExit exception should be raised and
    #      the exit status should be 2 and
    #      the beginning of stderr should match the expected error message
    assert int(str(e.value)) == 1
    assert err[0:eel] == expected_err


def test_log_fatal_and_exit(capfd, tested):
    # GIVEN the expected output to stderr
    expected_err = ("CRITICAL No handlers could be found for logger \"{0}\""
                    "\nCRITICAL (2) test_log_fatal_and_exit\n"
                    .format(tested))
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
    #      stderr should match the expected error message
    assert int(str(e.value)) == 2
    assert err == expected_err


def test_verify_root(capfd):
    # GIVEN the expected output to stderr
    expected_err = ("(77) Must be root or equivalent (ex. sudo).")
    # WHEN ops_utils.verify_root() is invoked as a non-root user
    with pytest.raises(ops_utils.Fatal) as e:
        ops_utils.verify_root()
    out, err = capfd.readouterr()
    # THEN the exception message should match the expected error message
    assert str(e.value) == expected_err
