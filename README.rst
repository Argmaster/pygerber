========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pygerber/badge/?style=flat
    :target: https://pygerber.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/Argmaster/pygerber.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/Argmaster/pygerber

.. |codecov| image:: https://codecov.io/gh/Argmaster/pygerber/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Argmaster/pygerber

.. |version| image:: https://img.shields.io/pypi/v/pygerber.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pygerber

.. |wheel| image:: https://img.shields.io/pypi/wheel/pygerber.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pygerber

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pygerber.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pygerber

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pygerber.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pygerber

.. |commits-since| image:: https://img.shields.io/github/commits-since/Argmaster/pygerber/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/Argmaster/pygerber/compare/v0.0.0...master



.. end-badges

Python package for 2D and 3D rendering of GerberX3 files.

* Free software: MIT license

Installation
============

::

    pip install pygerber

You can also install the in-development version with::

    pip install https://github.com/Argmaster/pygerber/archive/master.zip


Documentation
=============


https://pygerber.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
