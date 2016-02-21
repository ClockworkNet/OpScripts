# vim: set fileencoding=utf-8 :

"""Unit Tests
"""

# Standard Library
from __future__ import absolute_import, division, print_function
import os
import sys

# Third-party
import pytest

# Local/library specific
from opscripts.notify.email import v2 as ops_notify_email


@pytest.fixture(scope="function")
def prog(request):
    prog = os.path.basename(sys.argv[0])
    return prog


def test_message_send_smtpserver(prog, smtpserver):
    # GIVEN email message parameters and the expected output
    address = "<-pytestsmtpserver->"
    subject = "Test - disregard"
    body = "This is a test message"
    expected_out = ("Auto-Submitted: auto-replied"
                    "\nFrom: {0}"
                    "\nSubject: {1}"
                    "\nTo: {2}"
                    "\nX-Mailer: {3}"
                    "\n\n{4}"
                    .format(address, subject, address, prog, body))
    # WHEN the message object is created via ops_notify_email.Message and
    #      message.send is invoked with smtpserver
    message = ops_notify_email.Message(prog, subject, body)
    message.send(address, [address], host=smtpserver.addr[0],
                 port=smtpserver.addr[1])
    # THEN there should be a single email in smtpserver.outbox and
    #      the contents of the email should match the expected output
    assert len(smtpserver.outbox) == 1
    assert expected_out == smtpserver.outbox[0].as_string()


def test_message_send_dryrun(capfd, prog):
    # GIVEN email message parameters and the expected output
    address = "<-dryrun->"
    subject = "Test - disregard"
    body = "This is a test message"
    dryrun = True
    expected_out = ("Auto-Submitted: auto-replied"
                    "\nFrom: {0}"
                    "\nSubject: {1}"
                    "\nTo: {2}"
                    "\nX-Mailer: {3}"
                    "\n\n{4}\n\n"
                    .format(address, subject, address, prog, body))
    # WHEN the message object is created via ops_notify_email.Message and
    #      message.send is invoked with dryrun and
    #      the output is captured
    message = ops_notify_email.Message(prog, subject, body)
    message.send(address, [address], dryrun=dryrun)
    out, err = capfd.readouterr()
    # THEN stdout should match the expected output
    assert expected_out == out
