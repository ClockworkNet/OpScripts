# vim: set fileencoding=utf-8 :

"""OpScripts configuration library (thin wrapper over ConfigArgParse)
"""

# Standard library
from __future__ import absolute_import, division, print_function
import os.path
import sys

# Third-party
import configargparse

# Local/library specific
from opscripts.notify.email import v2 as ops_notify_email


def OpsConfigArgParse(**kwargs):
    """Wrap configargparse.ArgumentParser so that:
    - default_config_path includes /etc/opscripts/SCRIPTNAME.yaml.
    - add_config_file_help default to False
    - ignore_unknown_config_file_keys default to True
    - provide shorthand for adding common arguments

    Returns ArgumentParser object and default_config_path list
    """
    add_args = dict()
    prog = os.path.basename(sys.argv[0])
    default_conf_name = "%s.%s" % (os.path.splitext(prog)[0], "yaml")
    default_conf_path = os.path.join("/etc/opscripts", default_conf_name)
    add_program_name = False
    if "add_args" in kwargs:
        add_args = kwargs["add_args"]
        del kwargs["add_args"]
    if "add_config_file_help" not in kwargs:
        kwargs["add_config_file_help"] = False
    if "default_config_files" not in kwargs:
        kwargs["default_config_files"] = [default_conf_path]
    else:
        kwargs["default_config_files"] += [default_conf_path]
        default_conf_path = kwargs["default_config_files"]
    if "ignore_unknown_config_file_keys" not in kwargs:
        kwargs["ignore_unknown_config_file_keys"] = True
    if "program_name" not in kwargs:
        add_program_name = True

    cap = configargparse.ArgumentParser(**kwargs)

    # add_args
    if "EMAIL" in add_args and add_args["EMAIL"] is True:
        add_args["email-from"] = True
        add_args["email-host"] = True
        add_args["email-port"] = True
        add_args["email-to"] = True
    if "config" in add_args and add_args["config"] is True:
        cap.add_argument("-c", "--config", is_config_file=True,
                         help="Config file path. Default: {0}"
                         .format(default_conf_path))
    if "dryrun" in add_args and add_args["dryrun"] is True:
        cap.add_argument("-n", "--dryrun", action="store_true",
                         help="Dry run: do not make any changes.")
    if "email-from" in add_args and add_args["email-from"] is True:
        cap.add_argument("--email-from", metavar="EMAIL",
                         help="Email sender.")
    if "email-host" in add_args and add_args["email-host"] is True:
        cap.add_argument("--email-host", metavar="HOST",
                         default=ops_notify_email.DEFAULT_HOST,
                         help="Email host used to send messages.")
    if "email-port" in add_args and add_args["email-port"] is True:
        cap.add_argument("--email-port", metavar="PORT", type=int,
                         default=ops_notify_email.DEFAULT_PORT,
                         help="Email port used to send messages.")
    if "email-to" in add_args and add_args["email-to"] is True:
        cap.add_argument("--email-to", metavar="EMAILS", action="append",
                         help="Email recipients. May be specified multiple"
                         " times.")
    if "quiet" in add_args and add_args["quiet"] is True:
        raise Exception("quiet is no longer supported. Use verbosity"
                        " instead.")
    if "verbose" in add_args and add_args["verbose"] is True:
        raise Exception("verbose is no longer supported. Use verbosity"
                        " instead.")
    if "verbosity" in add_args and add_args["verbosity"] is True:
        cap.add_argument("-q", "--quiet", action="append_const", const=10,
                         dest="verbosity",
                         help="Decrease verbosity. Can be specified multiple"
                         " times.")
        cap.add_argument("-v", "--verbose", action="append_const", const=-10,
                         dest="verbosity",
                         help="Increase verbosity. Can be specified multiple"
                         " times.")

    # miscellaneous
    if add_program_name:
        cap.set_defaults(program_name=prog)

    return cap


def parse_args(cap, args=None, namespace=None):
    """Wrap parse_args to allow additional logic:
    - Only require --email_from/--email-to when not doing a dryrun
    """
    args = cap.parse_args(args=args, namespace=namespace)
    if "dryrun" in args and "email_from" in args:
        if not args.dryrun:
            if not args.email_from:
                cap.error("error: argument --email-from is required")
            if not args.email_to:
                cap.error("error: argument --email-to is required")
        else:
            if not args.email_from:
                args.email_from = "<-dryrun->"
            if not args.email_to:
                args.email_to = ["<-dryrun->"]
    return args
