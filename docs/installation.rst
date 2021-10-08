PyGerber Installation
=====================

PyGerber is available on PyPI and can be obtained via pip

.. code:: bash

    pip install pygerber

You can also install the in-development version from github with

.. code:: bash

    pip install https://github.com/Argmaster/pygerber/archive/main.zip

Blender dependency issue mentioned in previous releases was resolved by using
`PyR3 package <https://pypi.org/project/PyR3/>`_ which provides Blender.
**However, blender has to be installed independently from package by calling PyR3.install_bpy script**::

    python -m PyR3.install_bpy

Before You try to use 3D rendering.
