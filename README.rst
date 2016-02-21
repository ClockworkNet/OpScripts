OpScripts
=========

Python libraries to assist with writing Linux Ops scripts.


Python Compatibility
====================

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

- Unit Tests

  - `pytest`_
  - `pytest-catchlog`_
  - `pytest-flakes`_
  - `pytest-localserver`_
  - `pytest-pep8`_

.. _`ConfigArgParse`: https://github.com/bw2/ConfigArgParse
.. _`PyYAML`: http://pyyaml.org/wiki/PyYAML
.. _`ordereddict`: https://pypi.python.org/pypi/ordereddict/1.1
.. _`pytest`: http://pytest.org/latest/
.. _`pytest-catchlog`: https://pypi.python.org/pypi/pytest-catchlog
.. _`pytest-flakes`: https://pypi.python.org/pypi/pytest-flakes
.. _`pytest-localserver`: https://pypi.python.org/pypi/pytest-localserver
.. _`pytest-pep8`: http://pypi.python.org/pypi/pytest-pep8


License
=======

- `<LICENSE>`_ (`MIT License`_)

.. _`MIT License`: http://www.opensource.org/licenses/MIT
