#############################
 Project Specification files
#############################

So called **specfiles contains description of project to be rendered**.
The parameters that can be used in them differ depending on whether you
are rendering in 2D or 3D Specfiles can be written in one of three
languages: **JSON**, **YAML** and **TOML**. You have to indicated which
one of them was used by using either corresponding flag, *(--yaml for
YAML e.t.c)* when using CLI or appropriate function *(render_from_yaml()
for YAML e.t.c)*.

***************************
 Specfile for 2D rendering
***************************

2D spec top level parameters
============================

At top level **specfile** contains a *dictionary* with following keys:

   -  ``dpi`` - integer, DPI of output image, *optional*, **defaults to
      600**,

   -  ``ignore_deprecated`` - bool, if false, causes Gerber parser to
      halt after encountering deprecated syntax, *optional*, **defaults
      to True**,

   -  ``layers`` - list of layers, *mandatory*, each layer is a
      *dictionary* with following keys

         -  ``file_path``, string, path to Gerber source file,
            *mandatory*,
         -  ``colors``, *optional*, see :ref:`usage/specfile:Defining
            colors for layer`

Defining colors for layer
=========================

``colors`` layer dictionary param can be omitted, then color will be
determined from Gerber file name. Chosen color will be one of
:ref:`usage/specfile:Predefined colors`, the first whose name will be
found in the filename.

``colors`` can also be set to *string*, which have to be one of
:ref:`usage/specfile:Predefined colors`.

Third option is to set colors manually via *dictionary*, then dictionary
has following keys, whose values ​​are lists of 3 or 4 integers in range
0-255 representing RGB / RGBA colors

   -  ``dark`` - *mandatory*, no default value
   -  ``clear`` - *optional*, defaults to transparent
   -  ``background`` *optional*, defaults to transparent

Predefined Colors
=================

Following predefined colors are available:
   -  ``silk`` white, transparent, transparent
   -  ``paste_mask`` gray, transparent, transparent
   -  ``solder_mask`` light gray, transparent, transparent
   -  ``copper`` green, green (lighter), transparent
   -  ``orange`` orange, transparent, transparent
   -  ``green`` green, green (darker), transparent
   -  ``debug`` strange, strange, transparent

Example JSON specfile
=====================

.. literalinclude:: ../../tests/gerber/pillow/specfile.json
   :language: json
<<<<<<< HEAD
=======
   :name: specfile.json
>>>>>>> 3a25005dd3b68d7c0ae7d3f513678a44364b3f67
   :caption: tests/gerber/pillow/specfile.json

***************************
 Specfile for 3D rendering
***************************

3D spec top level parameters
============================

At top level specfile contains a dictionary with following keys:
   -  ``ignore_deprecated`` - bool, if false, causes Gerber parser to
      halt after encountering deprecated syntax, *optional*, **defaults
      to True**,

   -  ``scale`` - float, output scale, *optional*, **defaults to 1000**,
      not yet modifiable.

   -  ``layers`` - list of layers, *mandatory*, each layer is a
      *dictionary* with following keys

         -  ``file_path``, string, path to Gerber source file,
            *mandatory*,
         -  ``structure``, *optional*, see :ref:`usage/specfile:Defining
            structure of a layer`

Defining structure of a layer
-----------------------------

``structure`` parameter can be omitted, then structure will be
determined from Gerber file name. Chosen structure will be one of
:ref:`usage/specfile:Predefined layer structures`, the first whose name
will be found in the filename.

Otherwise it can be a string containing name of one of
:ref:`usage/specfile:Predefined layer structures`.

Last possible option is to use a dictionary with following keys:
   -  ``material`` - dictionary with blender `BSDF node parameters
      <https://pyr3.readthedocs.io/en/latest/reference/PyR3.shortcut.html#pyr3-shortcut-material-module>`_.
      Only exception from typical node parameters is that colors are
      lists integers in range 0-255, **not** floats 0.0 - 1.0

   -  ``thickness`` - thickness of layer in millimeters as float.

Predefined layer structures
---------------------------

Following predefined layer structure are available:
   -  ``silk`` 0.04mm, rough, non-metalic, white
   -  ``paste_mask`` 0.1mm, metallic, partially rough, gray
   -  ``solder_mask`` 0.1mm, metallic, partially rough, gray (lighter)
   -  ``copper`` 0.78mm, metallic, rough, green
   -  ``green`` 0.78mm, default, green
   -  ``debug`` 0.78mm, default, strange
   -  ``debug2`` 0.78mm, default, strange
   -  ``debug3`` 0.78mm, default, strange

Example YAML specfile
=====================

.. literalinclude:: ../../tests/gerber/blender/specfile.yaml
   :language: yaml
   :caption: tests/gerber/blender/specfile.yaml
