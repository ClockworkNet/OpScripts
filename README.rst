OpScripts
=========

Python libraries to assist with writing Linux Ops scripts.


Python Compatiblity
===================

This library currently requires compatibility with:

- 2.6
- 2.7
- 3.4

However, additional versions are tested automatically:

.. image:: https://travis-ci.org/ClockworkNet/OpScripts.svg?branch=master
    :target: https://travis-ci.org/ClockworkNet/OpScripts


API Versioning
==============

Each module is versioned so that they can undergo significant changes without
impacting the function and stability of the scripts that use them.

For example::

    from opscripts.config import v5 as ops_config
    from opscripts.logging import v2 as ops_logging
    from opscripts.utils import v4 as ops_utils

For a more in-depth examples, see the:

- `<example.py>`_
- `<example_notify_email.py>`_
- `<example_yaml.py>`_


Dependencies
============

- ``opscripts.config``

  - `ConfigArgParse`_

- ``opscripts.yaml``

  - `PyYAML`_
  - `ordereddict`_ (only required by Python 2.6)

.. _`ConfigArgParse`: https://github.com/bw2/ConfigArgParse
.. _`PyYAML`: http://pyyaml.org/wiki/PyYAML
.. _`ordereddict`: https://pypi.python.org/pypi/ordereddict/1.1


License
=======

- `<LICENSE>`_ (`MIT License`_)

.. _`MIT License`: http://www.opensource.org/licenses/MIT
