#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""Script_description_goes_here
"""

# Standard library
from __future__ import absolute_import, division, print_function
import logging
import sys

# Local/library specific
from opscripts.config import v5 as ops_config
from opscripts.logging import v2 as ops_logging
from opscripts.utils import v7 as ops_utils


LOG = logging.getLogger(__name__)


def setup():
    """Instantiate and configure configargparse and logging.

    Return configargsparse namespace.
    """
    add_args = {"config": True, "dryrun": True, "verbosity": True}
    cap = ops_config.OpsConfigArgParse(description=__doc__, add_args=add_args)
    logger = ops_logging.OpScriptsLogging(cap.prog)
    args = ops_config.parse_args(cap)
    logger.dryrun(args.dryrun)
    logger.set_log_level(args.verbosity)
    logger.remove_syslog_handler()
    LOG.warning("disabled logging to syslog")
    LOG.debug("args.program_name: {}".format(args.program_name))
    return args


def main():
    args = setup()  # noqa
    ops_utils.verify_root()
    ops_utils.request_confirmation(timeout=20)
    LOG.critical("test message to demonstrate use of logging module root"
                 " logger")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e.code)
    except KeyboardInterrupt:
        ops_utils.log_ctrlc_and_exit()
    except ops_utils.Fatal:
        ops_utils.log_fatal_and_exit()
    except:
        ops_utils.log_exception_and_exit()
