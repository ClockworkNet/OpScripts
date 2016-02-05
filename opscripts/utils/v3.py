# vim: set fileencoding=utf-8 :

"""OpScripts utilities library
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import logging
import os
import random
import select
import sys
import traceback


LOG = logging.getLogger(__name__)


class Fatal(Exception):
    def __init__(self, message, code=None):
        self.code = code if code else 1
        message = "({0}) {1}".format(self.code, message)
        super(Fatal, self).__init__(message)


def log_ctrlc_and_exit():
    print(file=sys.stderr)
    LOG.info("(130) Halted via KeyboardInterrupt.")
    sys.exit(130)


def log_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    name = exc_value.__class__.__name__
    data = traceback.extract_tb(exc_traceback)
    trace_bottom = ": ".join(str(i) for i in data[0])
    trace_top = ": ".join(str(i) for i in data[-1])
    LOG.critical("(1) {0}: {1}:  {2}  ...  {3}"
                 .format(name, exc_value, trace_top, trace_bottom))


def log_exception_and_exit(exit_status=1):
    log_exception()
    sys.exit(exit_status)


def log_fatal_and_exit():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    LOG.critical(exc_value)
    sys.exit(exc_value.code)


def request_confirmation(timeout=30):
    """Request the operator input the displayed random number to confirm the
    script should make the changes requested. Each attempt fails if the
    timeout is reached.

    Exits with an error after five failures.
    """
    try:
        timeout = float(timeout)
    except:
        raise Fatal("request_confirmation timeout must be a number",
                    os.EX_NOPERM)
    random_int = random.randint(10000, 99999)
    message = ("To continue, please enter the number '%d' within %d"
               " seconds:" % (random_int, timeout))
    i = 0
    while i < 5:
        i += 1
        print(message,)
        read_obj, w, x = select.select([sys.stdin], list(), list(), timeout)
        if read_obj:
            response = sys.stdin.readline().strip()
            try:
                response = int(response)
            except ValueError:
                pass
            except:
                raise
            if response == random_int:
                return
    raise Fatal("Failed to provide confirmation input.", os.EX_NOPERM)


def verify_root():
    """Verify script is being run as root.
    """
    if not os.geteuid() == 0:
        raise Fatal("Must be root or equivalent (ex. sudo).", os.EX_NOPERM)
