#!/bin/bash
echo 'Current Versions
================
config        v6
logging       v2
notify.email  v3
utils         v7
yaml          v1
'
config='config import v[1-5]'
logging='logging import v1'
notify_email='notify[.]email import v[1-2]'
utils='utils import v[1-6]'
regex="^from opscripts[.](${config}|${logging}|${notify_email}|${utils})"
ack --python "${regex}"
