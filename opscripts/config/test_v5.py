# vim: set fileencoding=utf-8 :

"""Unit Tests
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import os.path
import sys

# Third-party
import pytest

# Local/library specific
from . import v5 as ops_config


@pytest.fixture(scope="function")
def prog(request):
    prog = os.path.basename(sys.argv[0])
    return prog


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


def test_config_email_missing_required():
    # GIVEN ops_config initialization
    add_args = {"EMAIL": True, "dryrun": True}
    cap = ops_config.OpsConfigArgParse(add_args=add_args)
    # WHEN command line arguments are empty
    cmd_args = list()
    # THEN parsing the arguments should raise an exception because neither
    #      --dryrun nor --email-from and --email-to were specified
    with pytest.raises(SystemExit):
        args = ops_config.parse_args(cap, args=cmd_args)
        assert args


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
