.. image:: https://raw.githubusercontent.com/Argmaster/pygerber/main/docs/_static/pygerber_logo.png

========
Overview
========

.. start-badges

|docs| |travis| |codecov| |version| |wheel| |supported-versions| |supported-implementations| |commits-since|

.. |docs| image:: https://readthedocs.org/projects/pygerber/badge/?style=flat
    :target: https://pygerber.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/Argmaster/pygerber.svg?branch=v0.0.1
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/Argmaster/pygerber

.. |codecov| image:: https://api.travis-ci.com/Argmaster/pygerber.svg?branch=v0.0.1
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/Argmaster/pygerber/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/Argmaster/pygerber/compare/v0.0.1...main

.. end-badges

PyGerber is a Python library for 2D and 3D rendering of Gerber X3 files.
It is completely written in Python, and only dependencies are limiting its portability.

*3D rendering is still under development, it will arrive at next major release. (v1.0.0)*

**This package is a Free Software; it is released under MIT license**. Be aware that dependencies might be using different licenses.

PyGerber offers a CLI and API for Python to allow easy rendering of Gerber files.
Parser was build with GBR X3 format in mind, however, it has extensive
support for older standards and deprecated features.
Package is using third party libraries for low level drawing and mesh
creation.

*PyGerber's parser was not ment to be used by package users, but there are no obstacles preventing
you from using it. However, stability of the API is not guaranteed between minor releases (I'll do my
best to make it stable among patches).*

Installation
============

PyGerber is available on PyPI and can be obtained via pip

.. code:: bash

    pip install pygerber

Be aware that this will **only install general and 2D rendering dependencies**, as
**bpy (Blender) is not officially released as Python package**. You have to obtain
it yourself, which, for example, you can archive with help of guides contained in
this `repository <https://github.com/Argmaster/pyr3>`_.


You can also install the in-development version from github with

.. code:: bash

    pip install https://github.com/Argmaster/pygerber/archive/main.zip

Same Blender dependency issue applies to this installation method.

Compatibility
=============

PyGerber officially supports only Python 3.9, but 2D rendering should be also available for
3.8 and 3.7, as long as Pillow provides support for those versions. 3D rendering is not
possible on those versions of Python due to compatibility issues of Blender binaries and Blender's API changes.

Documentation
=============

Documentation of this library is available at https://pygerber.readthedocs.io/

Development
===========

To run all the tests, just run::

    tox

To see all the tox environments::

    tox -l

To only build the docs::

    tox -e docs

To build and verify that the built package is proper and other code QA checks::

    tox -e check

To build sdist, and bdist_wheel::

    python setup.py clean --all sdist bdist_wheel

To make a release of the project on PyPI, assuming you got some distributions in dist/, the most simple usage is::

    twine upload --skip-existing dist/*.whl dist/*.gz dist/*.zip

Credits
=======

Structure of this project was created using cookiecutter template `cookiecutter-pylibrary <https://github.com/ionelmc/cookiecutter-pylibrary>`_.
I'm very grateful to Ionel Cristian Mărieș for its creation.