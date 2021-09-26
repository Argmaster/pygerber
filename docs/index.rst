==============================
PyGerber package documentation
==============================

PyGerber is a tool for parsing and rendering Gerber files

It offers a CLI and API for Python to allow easy rendering of Gerber files.
Parser was build with GBR X3 format in mind, however, it has extensive
support for older standards and deprecated features.
External libraries are used for low-level drawing operations:

- `pillow <https://python-pillow.org/>`_ for 2D rendering, available on PyPI
- `bpy (blender) <https://www.blender.org/>`_ for 3D rendering, requires manual installation.

`3D rendering is still under development, it will arrive at next major release.`

========
Contents
========

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   reference/index
   contributing
   authors
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
