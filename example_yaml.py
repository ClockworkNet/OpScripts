#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Standard library
from __future__ import absolute_import, division, print_function
import logging
import sys
try:
    from collections import OrderedDict     # Python 2.7+
except ImportError:
    from ordereddict import OrderedDict     # Python 2.6

# Third-party
import yaml

# Local/library specific
from opscripts.config import v3 as ops_config
from opscripts.logging import v1 as ops_logging
from opscripts.utils import v2 as ops_utils
from opscripts.yaml import v1 as ops_yaml


LOG = logging.getLogger(__name__)
yaml.SafeDumper.add_representer(OrderedDict, ops_yaml.odict_rep)


def setup():
    """Instantiate and configure configargparse and logging.

    Return configargsparse namespace.
    """
    cap = ops_config.OpsConfigArgParse(description=__doc__)
    logger = ops_logging.OpScriptsLogging(cap.prog)
    args = cap.parse_args()
    args.program_name = cap.prog
    logger.remove_syslog_handler()
    return args


def main():
    args = setup()
    doc = OrderedDict()
    doc["one"] = "alfa"
    doc["two"] = ["bravo", "charlie", "delta"]
    doc["three"] = "echo"
    print(yaml.safe_dump(doc, indent=4, default_flow_style=False))


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
