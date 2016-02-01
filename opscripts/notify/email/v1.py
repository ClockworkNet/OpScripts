# vim: set fileencoding=utf-8 :

"""OpScripts notification via email library.
"""

# Standard library
from __future__ import absolute_import, division, print_function
from six import iteritems
import smtplib


class Message():
    def __init__(self, program_name, subject, body, headers=dict()):
        self.body = "{0}\n".format(body.strip())
        self.headers = headers
        headers_keys = list()
        for key in headers.keys():
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

    def _compile_message(self, sender, rcpts):
        headers = self.headers
        headers["To"] = ", ".join(rcpts)
        headers["From"] = sender
        email_message = ""
        for header, value in iteritems(headers):
            email_message = "{0}\n{1}: {2}".format(email_message, header,
                                                   value)
        return "{0}\n\n{1}".format(email_message.strip(), self.body)

    def send(self, sender, rcpts, host="localhost", port=25, dryrun=False):
        email_message = self._compile_message(sender, rcpts)
        if dryrun:
            print(email_message)
        else:
            s = smtplib.SMTP(host, port)
            s.sendmail(sender, rcpts, email_message)
            s.quit()
