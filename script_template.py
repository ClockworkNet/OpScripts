#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""Script_description_goes_here
"""

# Standard library
from __future__ import absolute_import, division, print_function
import logging
try:
    from collections import OrderedDict     # Python 2.7+
except ImportError:
    from ordereddict import OrderedDict     # Python 2.6

# Third-party
import yaml

# Local/library specific
from opscripts.config import v2 as ops_config
from opscripts.logging import v1 as ops_logging
from opscripts.utils import v2 as ops_utils
from opscripts.yaml import v1 as ops_yaml


LOG = logging.getLogger(__name__)
yaml.SafeDumper.add_representer(OrderedDict, ops_yaml.odict_rep)


def setup():
    """Instantiate and configure configargparse and logging.

    Return configargsparse namespace.
    """
    add_args = {"config": True, "dryrun": True, "verbose": True}
    cap = ops_config.OpsConfigArgParse(description=__doc__, add_args=add_args)
    logger = ops_logging.OpScriptsLogging(cap.prog)
    args = cap.parse_args()
    args.program_name = cap.prog
    logger.dryrun(args.dryrun)
    logger.set_log_level_verbose(args.verbose)
    LOG.warning("disabling logging to syslog")
    logger.remove_syslog_handler()
    return args


def main():
    args = setup()
    ops_utils.verify_root()
    ops_utils.request_confirmation(timeout=20)
    LOG.critical("test message to demonstrate use of logging module root"
                 " logger")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ops_utils.log_ctrlc_and_exit()
    except ops_utils.Fatal:
        ops_utils.log_fatal_and_exit()
    except:
        ops_utils.log_exception_and_exit()
