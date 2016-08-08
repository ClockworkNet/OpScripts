# vim: set fileencoding=utf-8 :

"""Unit Tests
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import logging
import os

# Third-party
try:
    import mock
except ImportError:
    import unittest.mock as mock
import pytest

# Local/library specific
from opscripts.utils import v7 as ops_utils

MODULE = "opscripts.utils.v7"
DOC = """\
Alfa        Bravo    Charlie
----        -----    -------
apple           1          x
banana         22  xxxxxxxxx
Clementine    333         xx\
"""


def _get_job_mock(exit_status, stdout, stderr):
    """Set up a mock process as return from Popen()"""
    job_mock = mock.Mock()
    b_stdout = stdout.encode()
    b_stderr = stderr.encode()
    attrs = {"wait.return_value": exit_status,
             "stdout.read.return_value": b_stdout,
             "stderr.read.return_value": b_stderr}
    job_mock.configure_mock(**attrs)
    return job_mock


@mock.patch("os.link")
def test_back_up_file_success(mock_link):
    # GIVEN I have a legitimate file to back up
    file = "/foo/bar/baz.py"

    # WHEN I back it up
    backup_file = ops_utils.back_up_file(file)

    # THEN I get the path to the backup
    assert backup_file == "/foo/bar/baz.py_orig"
    mock_link.assert_called_with(file, backup_file)


@mock.patch("os.link")
def test_back_up_file_rel_success(mock_link):
    # GIVEN I have a relative file to back up
    file = "baz.py"

    # WHEN I back it up
    backup_file = ops_utils.back_up_file(file)

    # THEN I get the full path to the backup
    assert backup_file == os.path.join(os.getcwd(), file + "_orig")
    mock_link.assert_called_with(file, backup_file)


@mock.patch("os.link")
def test_back_up_file_custom_suffix(mock_link):
    # GIVEN I have a legitimate file to back up
    file = "baz.py"
    suffix = "_bak"
    target_dir = "/foo/bar/"

    # WHEN I specify a custom dir and suffix
    backup_file = ops_utils.back_up_file(file, target_dir, suffix)

    # THEN the backup path reflects them
    assert backup_file == os.path.join(target_dir, file + suffix)
    mock_link.assert_called_with(file, backup_file)


@mock.patch("os.link")
def test_back_up_file_bad_file(mock_link):
    # GIVEN I have a path to a directory
    file = "/foo/bar/"

    # WHEN I back it up
    backup_file = ops_utils.back_up_file(file)

    # THEN we do not attempt to link
    assert backup_file is False
    assert mock_link.called is False


@mock.patch("os.link")
def test_back_up_file_bad_input(mock_link):
    # GIVEN I have an integer
    file = 123

    # WHEN I back it up
    # THEN we explode and do not attempt to link
    with pytest.raises(AttributeError):
        ops_utils.back_up_file(file)

    assert mock_link.called is False

    file = None
    with pytest.raises(AttributeError):
        ops_utils.back_up_file(file)

    assert mock_link.called is False


def test_exec_cmd_debug_success():
    # GIVEN the pwd command with root as the working directory
    cmd_args = ["pwd"]
    cwd = "/"
    uid = None
    gids = None
    # WHEN the command is executed
    exit_status, stdout, stderr = ops_utils.exec_cmd_debug(cmd_args, cwd=cwd,
                                                           uid=uid, gids=gids)
    # THEN exit status should be 0 and
    #      stdout should be root directory ("/")
    #      stderr should be empty
    assert exit_status == 0
    assert stdout == "/"
    assert stderr == ""


@mock.patch('subprocess.Popen')
def test_exec_cmd_fail_hard_fail(mock_subp):
    # GIVEN a command will exit with a non-zero return code
    cmd_args = ["foobar"]
    stdout = "This is output"
    stderr = "This is error"
    job_mock = _get_job_mock(1, stdout, stderr)
    mock_subp.return_value = job_mock

    # WHEN the command is executed
    # THEN a Fatal is raised
    with pytest.raises(ops_utils.Fatal):
        ops_utils.exec_cmd_fail_hard(cmd_args)


@mock.patch("subprocess.Popen")
def test_exec_cmd_fail_hard_success(mock_subp):
    # GIVEN a command will exit with a non-zero return code
    cmd_args = ["foobar"]
    stdout = "This is output"
    stderr = "This is error"
    job_mock = _get_job_mock(0, stdout, stderr)
    mock_subp.return_value = job_mock

    # WHEN the command is executed
    exit_status, out, err = ops_utils.exec_cmd_fail_hard(cmd_args)

    # THEN we receive the expected results of the command
    assert exit_status == 0
    assert out == stdout
    assert err == stderr


@mock.patch("select.select")
@mock.patch("sys.stdin.readline")
@mock.patch("subprocess.Popen")
def test_exec_cmd_fail_prompt_yes(mock_subp, mock_readline, mock_select):
    # GIVEN a command that exits non-zero
    cmd_args = ["foobar"]
    stdout = "This is output"
    stderr = "This is error"
    job_mock = _get_job_mock(1, stdout, stderr)
    mock_subp.return_value = job_mock
    mock_select.return_value = (True, None, None)

    # WHEN the command is executed and we answer "y" to continue
    mock_readline.return_value = "y"
    exit_status, out, err = ops_utils.exec_cmd_fail_prompt(cmd_args)

    # THEN we receive the expected results of the command
    assert mock_readline.called
    assert exit_status == 1
    assert out == stdout
    assert err == stderr


@mock.patch("select.select")
@mock.patch("sys.stdin.readline")
@mock.patch("subprocess.Popen")
def test_exec_cmd_fail_prompt_no(mock_subp, mock_readline, mock_select):
    # GIVEN a command that exits non-zero
    cmd_args = ["foobar"]
    stdout = "This is output"
    stderr = "This is error"
    job_mock = _get_job_mock(1, stdout, stderr)
    mock_subp.return_value = job_mock
    mock_select.return_value = (True, None, None)

    # WHEN the command is executed and we answer "n" to continue
    mock_readline.return_value = "n"

    # THEN a Fatal is raised
    with pytest.raises(ops_utils.Fatal):
        ops_utils.exec_cmd_fail_prompt(cmd_args)


@mock.patch("select.select")
@mock.patch("sys.stdin.readline")
@mock.patch("subprocess.Popen")
def test_exec_cmd_fail_prompt_many_bad(mock_subp, mock_readline, mock_select):
    # GIVEN a command that exits non-zero
    cmd_args = ["foobar"]
    stdout = "This is output"
    stderr = "This is error"
    job_mock = _get_job_mock(1, stdout, stderr)
    mock_subp.return_value = job_mock
    mock_select.return_value = (True, None, None)

    # WHEN the command is executed and we give non-y/n answers
    mock_readline.return_value = "x"

    # THEN a Fatal is raised after trying five times
    with pytest.raises(ops_utils.Fatal):
        ops_utils.exec_cmd_fail_prompt(cmd_args)

    assert mock_readline.call_count == 5


@mock.patch("subprocess.Popen")
def test_exec_cmd_fail_prompt_opt_yes(mock_subp):
    # GIVEN a command that exits non-zero
    cmd_args = ["foobar"]
    stdout = "This is output"
    stderr = "This is error"
    job_mock = _get_job_mock(1, stdout, stderr)
    mock_subp.return_value = job_mock

    # WHEN the command is executed with opts_yes = TRUE
    # THEN a Fatal is raised
    with pytest.raises(ops_utils.Fatal):
        ops_utils.exec_cmd_fail_prompt(cmd_args, opt_yes=True)


@mock.patch("select.select")
@mock.patch("sys.stdin.readline")
@mock.patch("subprocess.Popen")
def test_exec_cmd_fail_prompt_opt_force(mock_subp, mock_readline, mock_select):
    # GIVEN a command that exits non-zero
    cmd_args = ["foobar"]
    stdout = "This is output"
    stderr = "This is error"
    job_mock = _get_job_mock(1, stdout, stderr)
    mock_subp.return_value = job_mock
    mock_select.return_value = (True, None, None)

    # WHEN the command is executed with opt_force = True
    exit_status, _, _ = ops_utils.exec_cmd_fail_prompt(cmd_args,
                                                       opt_force=True)

    # THEN we receive the expected results of the command without prompting
    assert exit_status == 1
    assert mock_readline.called is False
    assert mock_select.called is False


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


def test_get_non_root_ids_fallback():
    # GIVEN provided fallback ids and
    #       invalid test_uids
    #       there are not sudo environment variables
    fallback_uid = 666
    fallback_gid = 1138
    test_uid1, test_uid2, test_uid3 = (None, 0, "")
    # WHEN get_non_root_ids is run
    uid1, gid1 = ops_utils.get_non_root_ids(test_uid1, fallback_uid,
                                            fallback_gid)
    uid2, gid2 = ops_utils.get_non_root_ids(test_uid2, fallback_uid,
                                            fallback_gid)
    uid3, gid3 = ops_utils.get_non_root_ids(test_uid3, fallback_uid,
                                            fallback_gid)
    # THEN the uids and gids will equal fallback values
    assert (uid1, gid1) == (fallback_uid, [fallback_gid])
    assert (uid2, gid2) == (fallback_uid, [fallback_gid])
    assert (uid3, gid3) == (fallback_uid, [fallback_gid])


def test_is_valid_hostname_one_trailing_dot():
    # GIVEN a valid hostname with one trailing dot
    chars = list()
    for i in list(range(63)):
        chars.append("a")
    hostname = "{0}.example.com.".format("".join(chars))
    # WHEN hostname validity is tested
    result = ops_utils.is_valid_hostname(hostname)
    # THEN result is True
    assert result is True


def test_is_valid_hostname_two_trailing_dots():
    # GIVEN an invalid hostname with two trailing dots
    hostname = "example.com.."
    # WHEN hostname validity is tested
    result = ops_utils.is_valid_hostname(hostname)
    # THEN result is False
    assert result is False


def test_is_valid_hostname_to_long():
    # GIVEN an invalid hostname that is too long (260 characters)
    labels = list()
    for i in list(range(26)):
        labels.append("a123456789")
    hostname = ".".join(labels)
    # WHEN hostname validity is tested
    result = ops_utils.is_valid_hostname(hostname)
    # THEN result is False
    assert result is False


def test_is_valid_hostname_all_numeric():
    # GIVEN an invalid hostname that contains only numbers
    hostname = "127.0.0.1"
    # WHEN hostname validity is tested
    result = ops_utils.is_valid_hostname(hostname)
    # THEN result is False
    assert result is False


def test_is_valid_hostname_label_to_long():
    # GIVEN an invalid hostname that is too long (260 characters)
    chars = list()
    for i in list(range(64)):
        chars.append("a")
    hostname = "{0}.example.com".format("".join(chars))
    # WHEN hostname validity is tested
    result = ops_utils.is_valid_hostname(hostname)
    # THEN result is False
    assert result is False


def test_is_valid_hostname_label_starts_with_dash():
    # GIVEN an invalid hostname that has a label that starts with a dash
    hostname = "-bad.example.com"
    # WHEN hostname validity is tested
    result = ops_utils.is_valid_hostname(hostname)
    # THEN result is False
    assert result is False


def test_is_valid_hostname_label_ends_with_dash():
    # GIVEN an invalid hostname that has a label that ends with a dash
    hostname = "bad-.example.com"
    # WHEN hostname validity is tested
    result = ops_utils.is_valid_hostname(hostname)
    # THEN result is False
    assert result is False


def test_is_valid_hostname_illegal_char():
    # GIVEN an invalid hostname that contains an illegal character
    hostname = "greater>than.example.com"
    # WHEN hostname validity is tested
    result = ops_utils.is_valid_hostname(hostname)
    # THEN result is False
    assert result is False


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
    expected_err = ("\nCRITICAL No handlers could be found for logger \"{0}\""
                    "\nINFO (130) Halted via KeyboardInterrupt.\n"
                    .format(MODULE))
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
