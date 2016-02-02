# vim: set fileencoding=utf-8 :

"""OpScripts confuration library (thin wrapper over ConfigArgParse)
"""

# Standard library
from __future__ import absolute_import, division, print_function
import os.path
import sys

# Third-party
import configargparse

# Local/library specific
from opscripts.notify.email import v1 as ops_notify_email


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

    cap = configargparse.ArgumentParser(**kwargs)

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
        cap.add_argument("--email-from", metavar="EMAIL", required=True,
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
                         required=True,
                         help="Email recipients. May be specified multiple"
                         " times.")
    if "quiet" in add_args and add_args["quiet"] is True:
        cap.add_argument("-q", "--quiet", action="count", default=0,
                         help="Decrease verbosity. Can be specified multiple"
                         " times.")
    if "verbose" in add_args and add_args["verbose"] is True:
        cap.add_argument("-v", "--verbose", action="count", default=0,
                         help="Increase verbosity. Can be specified multiple"
                         " times.")

    return cap
