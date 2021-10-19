.. image:: https://raw.githubusercontent.com/Argmaster/pygerber/main/docs/_static/project_logo.png
   :alt: Project Logo
   :align: center

##########
 Overview
##########

.. image:: https://img.shields.io/github/license/Argmaster/pygerber
   :alt: Package License
   :target: https://pypi.org/project/pygerber

.. image:: https://readthedocs.org/projects/pygerber/badge/?style=flat
   :alt: Documentation Status
   :target: https://pygerber.readthedocs.io/

.. image:: https://github.com/Argmaster/pygerber/actions/workflows/draft_release.yaml/badge.svg?style=flat
   :alt: Workflow Status
   :target: https://github.com/Argmaster/pygerber

.. image:: https://github.com/Argmaster/pygerber/actions/workflows/release_pr_tests.yaml/badge.svg?style=flat
   :alt: Workflow Status
   :target: https://github.com/Argmaster/pygerber

.. image:: https://codecov.io/gh/Argmaster/pygerber/branch/main/graph/badge.svg?token=VM09IHO13U
   :alt: Code coverage stats
   :target: https://codecov.io/gh/Argmaster/pygerber

.. image:: https://img.shields.io/github/v/release/Argmaster/pygerber?style=flat
   :alt: GitHub release (latest by date)
   :target: https://github.com/Argmaster/pygerber/releases/tag/1.1.0

.. image:: https://img.shields.io/github/commit-activity/m/Argmaster/pygerber
   :alt: GitHub commit activity
   :target: https://github.com/Argmaster/pygerber/commits/main

.. image:: https://img.shields.io/github/issues-pr/Argmaster/pygerber?style=flat
   :alt: GitHub pull requests
   :target: https://github.com/Argmaster/pygerber/pulls

.. image:: https://img.shields.io/github/issues-pr-closed-raw/Argmaster/pygerber?style=flat
   :alt: GitHub closed pull requests
   :target: https://github.com/Argmaster/pygerber/pulls

.. image:: https://img.shields.io/github/issues-raw/Argmaster/pygerber?style=flat
   :alt: GitHub issues
   :target: https://github.com/Argmaster/pygerber/issues

.. image:: https://img.shields.io/github/languages/code-size/Argmaster/pygerber
   :alt: GitHub code size in bytes
   :target: https://github.com/Argmaster/pygerber

.. image:: https://img.shields.io/pypi/v/pygerber?style=flat
   :alt: PyPI Package latest release
   :target: https://pypi.org/project/pygerber

.. image:: https://img.shields.io/pypi/wheel/pygerber?style=flat
   :alt: PyPI Wheel
   :target: https://pypi.org/project/pygerber

.. image:: https://img.shields.io/pypi/pyversions/pygerber?style=flat
   :alt: Supported versions
   :target: https://pypi.org/project/pygerber

.. image:: https://img.shields.io/pypi/implementation/pygerber?style=flat
   :alt: Supported implementations
   :target: https://pypi.org/project/pygerber

PyGerber is a Python library for 2D and 3D rendering of Gerber X3 files.
It is completely written in Python, and only dependencies are limiting
its portability.

**This package is a Free Software; it is released under MIT license**.
Be aware that dependencies might be using different licenses.

PyGerber offers a CLI and API for Python to allow easy rendering of
Gerber files. Parser was build with GBR X3 format in mind, however, it
has extensive support for older standards and deprecated features.
Package is using third party libraries for low level drawing and mesh
creation.

*PyGerber's parser was not mend to be used by package users, but there
are no obstacles preventing you from using it. However, stability of the
API is not guaranteed between minor releases (I'll do my best to make it
stable among patches).*

**************
 Installation
**************

PyGerber is available on PyPI and can be obtained via pip

.. code:: bash

   pip install pygerber

You can also install the in-development version from github with

.. code:: bash

   pip install https://github.com/Argmaster/pygerber/archive/main.zip

Blender dependency issue mentioned in previous releases was resolved by
using `PyR3 package <https://pypi.org/project/PyR3/>`_ which provides
Blender. **However, blender has to be installed independently from
package by calling PyR3.install_bpy script**:

.. code::

   python -m PyR3.install_bpy

Before You try to use 3D rendering.

***************
 Compatibility
***************

PyGerber officially runs on Python 3.9.* and only on this version.
However it may be possible to run 2D rendering on other Python versions
that are supported by Pillow.

I'll consider bringing Python 3.8 3D rendering support, but no sooner
than after implementation of full set of 3D rendering features and
macros support.

***************
 Documentation
***************

Documentation of this library is available at
https://pygerber.readthedocs.io/
