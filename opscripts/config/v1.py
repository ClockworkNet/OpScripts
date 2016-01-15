# vim: set fileencoding=utf-8 :

"""OpScripts confuration library (thin wrapper over ConfigArgParse)
"""

# Standard library
from __future__ import absolute_import, division, print_function
import os.path
import sys

# Third-party
import configargparse


def OpsConfigArgParse(**kwargs):
    """Wrap configargparse.ArgumentParser so that:
    - default_config_path includes /etc/opscripts/SCRIPTNAME.yaml.
    - add_config_file_help default to False

    Returns ArgumentParser object and default_config_path list
    """
    prog = os.path.basename(sys.argv[0])
    default_conf_name = "%s.%s" % (os.path.splitext(prog)[0], "yaml")
    default_conf_path = os.path.join("/etc/opscripts", default_conf_name)
    if "add_config_file_help" not in kwargs:
        kwargs["add_config_file_help"] = False
    if "default_config_files" not in kwargs:
        kwargs["default_config_files"] = [default_conf_path]
    else:
        kwargs["default_config_files"] += [default_conf_path]
        default_conf_path = kwargs["default_config_files"]
    cap = configargparse.ArgumentParser(**kwargs)
    return cap, default_conf_path
