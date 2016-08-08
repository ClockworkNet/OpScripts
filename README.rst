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
    from opscripts.utils import v7 as ops_utils

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

  - `mock`_ (only required by Python < 3.3)
  - `pytest`_
  - `pytest-catchlog`_
  - `pytest-colordots`_
  - `pytest-flakes`_
  - `pytest-localserver`_
  - `pytest-pep8`_
  - `pytest-pythonpath`_

.. _`ConfigArgParse`: https://github.com/bw2/ConfigArgParse
.. _`PyYAML`: http://pyyaml.org/wiki/PyYAML
.. _`ordereddict`: https://pypi.python.org/pypi/ordereddict/1.1
.. _`mock`: https://pypi.python.org/pypi/mock
.. _`pytest`: http://pytest.org/latest/
.. _`pytest-catchlog`: https://pypi.python.org/pypi/pytest-catchlog
.. _`pytest-colordots`: https://github.com/svenstaro/pytest-colordots
.. _`pytest-flakes`: https://pypi.python.org/pypi/pytest-flakes
.. _`pytest-localserver`: https://pypi.python.org/pypi/pytest-localserver
.. _`pytest-pep8`: http://pypi.python.org/pypi/pytest-pep8
.. _`pytest-pythonpath`: https://pypi.python.org/pypi/pytest-pythonpath


Testing Quick Start
===================

1. Change directory into repository (into same directory as where this README
   resides).
2. Install virtual environment::

    mkvirtualenv -a . -r tests/requirements.txt opscripts_test

   a. If installing requirements errors, update `pip`::

        pip install --upgrade pip

   b. Install requirements::

        pip install -r tests/requirements.txt

3. Run pytest::

    py.test

To test against alternate Python versions, it may be useful to create virtual
environments with an interpreter other than the one with which ``virtualenv``
was installed, e.g. for non-default python3::

    mkvirtualenv -a . -p $(which python3) -r tests/requirements.txt opscripts_test3


License
=======

- `<LICENSE>`_ (`MIT License`_)

.. _`MIT License`: http://www.opensource.org/licenses/MIT
