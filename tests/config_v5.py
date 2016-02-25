# vim: set fileencoding=utf-8 :

"""Unit Tests
"""

# TODO:
# - configargparse functionality
#   - config file
#   - environment

# Standard Library
from __future__ import absolute_import, division, print_function
import os.path
import sys

# Third-party
import pytest

# Local/library specific
from opscripts.config import v5 as ops_config


@pytest.fixture(scope="function")
def prog(request):
    prog = os.path.basename(sys.argv[0])
    return prog


def test_cap_simple(prog):
    # GIVEN ops_config
    # WHEN intialized without default_config_files
    cap = ops_config.OpsConfigArgParse()
    # THEN cap object's default_config_files should contain only the default
    #      added by OpsConfigArgParse and
    #      cap object's add_config_file_help should be False
    #      cap object's ignore_unknown_config_file_keys should be True
    assert cap._default_config_files == ["/etc/opscripts/py.yaml"]
    assert cap._add_config_file_help is False
    assert cap._ignore_unknown_config_file_keys is True


def test_cap_with_add_config_file_help(prog):
    # GIVEN ops_config
    # WHEN intialized with add_config_file_help as True
    cap = ops_config.OpsConfigArgParse(add_config_file_help=True)
    # THEN cap object's add_config_file_help should be False
    assert cap._add_config_file_help is True


def test_cap_with_default_config_files(prog):
    # GIVEN ops_config and specified conf_files
    conf_files = ["/conf1", ".conf2"]
    # WHEN intialized with specified default_config_files
    cap = ops_config.OpsConfigArgParse(default_config_files=conf_files)
    # THEN object's default_config_files should contain a combination of the
    #      specified configuration files and the default added by
    #      OpsConfigArgParse
    assert cap._default_config_files == ["/conf1", ".conf2",
                                         "/etc/opscripts/py.yaml"]


def test_cap_with_ignore_unknown_config_file_keys(prog):
    # GIVEN ops_config
    # WHEN intialized with ignore_unknown_config_file_keys
    cap = ops_config.OpsConfigArgParse(ignore_unknown_config_file_keys=False)
    # THEN object's ignore_unknown_config_file_keys should be False
    assert cap._ignore_unknown_config_file_keys is False


def test_config_basic(prog):
    # GIVEN ops_config initialization
    add_args = {"config": True, "dryrun": True, "verbosity": True}
    cap = ops_config.OpsConfigArgParse(add_args=add_args)
    # WHEN command line arguments are empty
    cmd_args = list()
    # THEN the args namespace should contain four items and
    #      it should contain config with value None and
    #      it should contain dryrun with value False and
    #      it should contain program_name with appropirate value and
    #      it should contain verbosity with value None
    args = ops_config.parse_args(cap, args=cmd_args)
    assert len(args._get_kwargs()) == 4
    assert "config" in args
    assert args.config is None
    assert "dryrun" in args
    assert args.dryrun is False
    assert "program_name" in args
    assert args.program_name == prog
    assert "verbosity" in args
    assert args.verbosity is None


def test_config_verbosity():
    # GIVEN ops_config initialization
    add_args = {"verbosity": True}
    cap = ops_config.OpsConfigArgParse(add_args=add_args)
    # WHEN command line has ten quiet flags and ten verbose flags
    cmd_args = ["-q"] * 5 + ["-v"] * 5
    verbosity = [10] * 5 + [-10] * 5
    # THEN parsing the arguments should raise an exception because neither
    #      --dryrun nor --email-from and --email-to were specified
    args = ops_config.parse_args(cap, args=cmd_args)
    assert "verbosity" in args
    assert args.verbosity == verbosity


def test_config_quiet_exception():
    # GIVEN the expected text and add_args containing quiet
    expected_text = ("quiet is no longer supported. Use verbosity instead.")
    add_args = {"quiet": True, }
    # WHEN OpsConfigArgParse is invoked with quiet
    with pytest.raises(Exception) as e:
        ops_config.OpsConfigArgParse(add_args=add_args)
    # THEN a Exception should be raised and
    #      the exception value should match the expected text
    assert str(e.value) == expected_text


def test_config_verbose_exception():
    # GIVEN the expected text and add_args containing verbose
    expected_text = ("verbose is no longer supported. Use verbosity instead.")
    add_args = {"verbose": True, }
    # WHEN OpsConfigArgParse is invoked with verbose
    with pytest.raises(Exception) as e:
        ops_config.OpsConfigArgParse(add_args=add_args)
    # THEN a Exception should be raised and
    #      the exception value should match the expected text
    assert str(e.value) == expected_text


def test_config_email_missing_email_from():
    # GIVEN ops_config initialization
    add_args = {"EMAIL": True, "dryrun": True}
    cap = ops_config.OpsConfigArgParse(add_args=add_args)
    # WHEN command line arguments are empty
    cmd_args = ["--email-to", "null"]
    # THEN parsing the arguments should raise an exception because neither
    #      --dryrun nor --email-from and --email-to were specified
    with pytest.raises(SystemExit):
        ops_config.parse_args(cap, args=cmd_args)


def test_config_email_missing_email_to():
    # GIVEN ops_config initialization
    add_args = {"EMAIL": True, "dryrun": True}
    cap = ops_config.OpsConfigArgParse(add_args=add_args)
    # WHEN command line arguments are empty
    cmd_args = ["--email-from", "null"]
    # THEN parsing the arguments should raise an exception because neither
    #      --dryrun nor --email-from and --email-to were specified
    with pytest.raises(SystemExit):
        ops_config.parse_args(cap, args=cmd_args)


def test_config_email_dryrun():
    # GIVEN ops_config initialization
    add_args = {"EMAIL": True, "dryrun": True}
    cap = ops_config.OpsConfigArgParse(add_args=add_args)
    # WHEN command line arguments contain --dryrun
    cmd_args = ["--dryrun"]
    # THEN parsing the arguments should succeed and
    #      the email address arguments should be set to "<-dryrun->"
    args = ops_config.parse_args(cap, args=cmd_args)
    assert "dryrun" in args
    assert args.dryrun is True
    assert "email_from" in args
    assert args.email_from == "<-dryrun->"
    assert "email_host" in args
    assert args.email_host == "localhost"
    assert "email_port" in args
    assert args.email_port == 25
    assert "email_to" in args
    assert args.email_to == ["<-dryrun->"]
