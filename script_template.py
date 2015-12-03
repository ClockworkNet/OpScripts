#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
"""Script_description_goes_here"""
# Standard library
from __future__ import print_function
import logging
import sys
# Third-party
# [...]
# Local/library specific
from opscripts.config import v1 as ops_config
from opscripts.logging import v1 as ops_logging
from opscripts.utils import v1 as ops_utils


def setup():
    """Instantiate and configure configargparse and logging.

    Return configargsparse namespace.
    """
    cap, default_conf_path = ops_config.OpsConfigArgParse(description=__doc__)
    logger = ops_logging.OpScriptsLogging(cap.prog)
    cap.add_argument("-c", "--config", is_config_file=True,
                     help="Config file path. Default: %s" % default_conf_path)
    cap.add_argument("-n", "--dryrun", action="store_true",
                     help="Dry run: do not make any changes.")
    cap.add_argument("-v", "--verbose", action="count", default=0,
                     help="Increase verbosity. Can be specified multiple"
                     " times.")
    args = cap.parse_args()
    args.program_name = cap.prog
    logger.dryrun(args.dryrun)
    logger.set_log_level_verbose(args.verbose)
    return args


def main():
    args = setup()
    ops_utils.verify_root()
    ops_utils.request_confirmation(timeout=20)
    logging.critical("test message to demonstrate use of root logger")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        logging.info("halted via KeyboardInterrupt.")
        sys.exit(130)
