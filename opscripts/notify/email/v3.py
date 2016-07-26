# vim: set fileencoding=utf-8 :

"""OpScripts notification via email library.
"""

# Standard library
from __future__ import absolute_import, division, print_function
import os
import smtplib
import socket

# Local/library specific
from opscripts.utils import v5 as ops_utils


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 25


class Message():
    def __init__(self, program_name=None, subject=None, body=None,
                 headers=None):
        """Initialize message object and verify arguments.
        """
        self.body = "{0}\n".format(body.strip("\n\r"))
        if headers:
            self.headers = headers
        else:
            self.headers = dict()
        headers_keys = list()
        for key in self.headers.keys():
            headers_keys.append(key.lower())
        if "to" in headers_keys:
            raise ValueError("The headers argument must not contain \"To\"."
                             " Recipients are set at send.")
        if "from" in headers_keys:
            raise ValueError("The headers argument must not contain \"From\"."
                             " Sender is set at send.")
        if "x-mailer" in headers_keys:
            raise ValueError("The headers argument must not contain"
                             " \"X-Mailer\". It must set via the program_name"
                             " argument.")
        else:
            self.headers["X-Mailer"] = program_name
        if "subject" in headers_keys:
            raise ValueError("The headers argument must not contain"
                             " \"Subject\". It must be set via the subject"
                             " argument.")
        else:
            self.headers["Subject"] = subject
        if "auto-submitted" not in headers_keys:
            self.headers["Auto-Submitted"] = "auto-replied"

    def _compile_message(self, sender, recipients):
        """Compile message from headers list (with sender and recipients
        added) and body.
        """
        headers = self.headers
        headers["To"] = ", ".join(recipients)
        headers["From"] = sender
        email_message = ""
        headers_keys = list(headers.keys())
        headers_keys.sort()
        for key in headers_keys:
            email_message = "{0}\n{1}: {2}".format(email_message, key,
                                                   headers[key])
        return "{0}\n\n{1}".format(email_message.strip(), self.body)

    def send(self, sender, recipients, host=DEFAULT_HOST, port=DEFAULT_PORT,
             dryrun=False):
        """Send compiled message via SMTP host:port.
        """
        if sender is None:
            raise TypeError("Message recipients is None, must be a"
                            " recipients (see --email-from help)")
        if recipients is None:
            raise TypeError("Message recipients is None, must be a list of"
                            " recipients (see --email-to help)")
        email_message = self._compile_message(sender, recipients)
        if dryrun:
            print(email_message)
        else:
            s = None
            try:
                s = smtplib.SMTP(host, port)
                s.sendmail(sender, recipients, email_message)
            except socket.error as e:
                #  8 nodename nor servname provided, or not known
                # 61 Connection refused
                if e.errno in (8, 61):
                    err_msg = ("Unable to connect to {0}:{1} - socket error"
                               " {2}: {3}."
                               .format(host, port, e.errno, e.strerror))
                    raise ops_utils.Fatal(err_msg, os.EX_UNAVAILABLE)
                else:
                    raise
            finally:
                if s:
                    s.quit()
