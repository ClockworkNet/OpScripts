.. image:: https://img.shields.io/badge/Supported%20by-Clockwork-ffcc00.svg
    :alt: badge: Supported by Clockwork
    :align: right
    :target: https://www.clockwork.com/

OpScripts
=========

.. image:: https://img.shields.io/pypi/v/OpScripts.svg
    :alt: badge: Python Package Index version
    :align: right
    :target: https://pypi.python.org/pypi/OpScripts
.. image:: https://img.shields.io/github/tag/ClockworkNet/OpScripts.svg
    :alt: badge: GitHub most recent tag
    :align: right
    :target: https://github.com/ClockworkNet/OpScripts/tags
Python libraries to assist with writing Linux Ops scripts.


Python Compatibility
====================

This library currently requires compatibility with:


.. image:: https://img.shields.io/pypi/pyversions/OpScripts.svg
    :alt: badge: Python Package Index supported Python versions
    :align: right
    :target: https://pypi.python.org/pypi/OpScripts
- 2.6
- 2.7
- 3.4

.. image:: https://img.shields.io/travis/ClockworkNet/OpScripts/master.svg
    :alt: badge: Travis CI master branch status
    :align: right
    :target: https://travis-ci.org/ClockworkNet/OpScripts
However, additional versions are tested automatically.


API Versioning
==============

Each module is versioned so that they can undergo significant changes without
impacting the function and stability of the scripts that use them.

For example::

    from opscripts.config import v6 as ops_config
    from opscripts.logging import v2 as ops_logging
    from opscripts.utils import v8 as ops_utils

For a more in-depth examples, see the:

- `<example.py>`_
- `<example_notify_email.py>`_
- `<example_yaml.py>`_


Dependencies
============

- ``opscripts.config``

  - `ConfigArgParse`_
  - `PyYAML`_

- ``opscripts.yaml``

  - `ordereddict`_ (only required by Python 2.6)
  - `PyYAML`_

- Unit Tests

  - `mock`_ (only required by Python < 3.3)
  - `pytest`_
  - `pytest-catchlog`_
  - `pytest-colordots`_
  - `pytest-flakes`_
  - `pytest-localserver`_
  - `pytest-pep8`_
  - `pytest-pep257`_
  - `pytest-pythonpath`_
  - `pytest-remove-stale-bytecode`_
  - `pytest-warnings`_

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
.. _`pytest-pep257`: https://pypi.python.org/pypi/pytest-pep257
.. _`pytest-remove-stale-bytecode`:
   https://bitbucket.org/gocept/pytest-remove-stale-bytecode/
.. _`pytest-warnings`: https://github.com/fschulze/pytest-warnings

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

    mkvirtualenv -a . -p $(which python3) -r tests/requirements.txt \
        opscripts_test3


License
=======

.. image:: https://img.shields.io/github/license/ClockworkNet/OpScripts.svg
    :alt: badge: GitHub license (MIT)
    :align: right
    :target: `MIT License`_
- `<LICENSE>`_ (`MIT License`_)

.. _`MIT License`: http://www.opensource.org/licenses/MIT
