#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Standard library
from __future__ import absolute_import, division, print_function
import logging
import sys

# Local/library specific
from opscripts.config import v5 as ops_config
from opscripts.logging import v2 as ops_logging
from opscripts.notify.email import v3 as ops_notify_email
from opscripts.utils import v7 as ops_utils


LOG = logging.getLogger(__name__)


def setup():
    """Instantiate and configure configargparse and logging.

    Return configargsparse namespace.
    """
    add_args = {"config": True, "EMAIL": True, "dryrun": True,
                "verbosity": True}
    cap = ops_config.OpsConfigArgParse(description=__doc__, add_args=add_args)
    logger = ops_logging.OpScriptsLogging(cap.prog)
    args = ops_config.parse_args(cap)
    logger.set_log_level(args.verbosity)
    logger.dryrun(args.dryrun)
    return args


def main():
    args = setup()
    subject = "Test - disregard"
    body = "This is a test message"
    message = ops_notify_email.Message(args.program_name, subject, body)
    message.send(args.email_from, args.email_to, dryrun=args.dryrun)


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
