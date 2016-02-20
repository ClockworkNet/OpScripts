# vim: set fileencoding=utf-8 :

"""OpScripts logging library
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import logging
import logging.handlers
import sys


class OpScriptsLogging(object):
    """OpScripts logging wrapper.
    """

    def __init__(self, program_name, log_level=logging.WARNING):
        """Initialize logging with screen and syslog handlers.
        """
        # Set up the logging system
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)

        # Screen Handler
        self.handler_screen = logging.StreamHandler()
        format_string = "%(levelname)s %(message)s"
        screen_format = logging.Formatter(format_string)
        self.handler_screen.setFormatter(screen_format)
        self.logger.addHandler(self.handler_screen)

        # Syslog Handler
        if sys.platform == "darwin":
            syslog = "/var/run/syslog"
        else:
            syslog = "/dev/log"
        self.handler_syslog = logging.handlers.SysLogHandler(syslog)
        format_string = "{0} %(levelname)s %(message)s".format(program_name)
        syslog_format = logging.Formatter(format_string)
        self.handler_syslog.setFormatter(syslog_format)
        self.logger.addHandler(self.handler_syslog)

    def dryrun(self, dryrun_enabled):
        """Update screen handler formatting to indicate dryrun and remove
        syslog handler.
        """
        if dryrun_enabled:
            format_string = "%(levelname)s (dryrun) %(message)s"
            screen_format = logging.Formatter(format_string)
            self.handler_screen.setFormatter(screen_format)
            self.logger.removeHandler(self.handler_syslog)

    def set_log_level(self, verbosity):
        """Set logging level based on verbosity level. Requires
        opscripts/config/v3 or later.
        """
        if not verbosity:
            return
        log_level = self.logger.getEffectiveLevel()
        for v in verbosity:
            log_level += v
        if log_level < 10:
            log_level = 10
        if log_level > 50:
            log_level = 50
        self.logger.setLevel(log_level)

    def set_log_level_quiet(self, quiet_count):
        raise Exception("set_log_level_quiet is no longer supported. Use"
                        " set_log_level and verbosity from config v4 or"
                        " later.")

    def set_log_level_verbose(self, verbose_count):
        raise Exception("set_log_level_verbose is no longer supported. Use"
                        " set_log_level and verbosity from config v4 or"
                        " later.")

    def remove_syslog_handler(self):
        """Remove logging to syslog.
        """
        self.logger.removeHandler(self.handler_syslog)
