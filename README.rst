OpScripts
=========

Python libraries to assist with writing Linux Ops scripts.


Python Version Target
=====================

This library currently targets Python version 2.6.

It has been tested with the following version of Python:

- 2.6.5
- 2.7.3, 2.7.6
- 3.4.3


API Versioning
==============

Each module is versioned so that they can undergo significant changes without
impacting the function and stability of the scripts that use them.

For example::

    from opscripts.config import v3 as ops_config
    from opscripts.logging import v1 as ops_logging
    from opscripts.utils import v2 as ops_utils

For a more in-depth examples, see the:

- `<script_template.py>`_
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
