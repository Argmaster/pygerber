#############################
 Project Specification files
#############################

So called **specfiles contains description of project to be rendered**. The
parameters that can be used in them differ depending on whether you are
rendering in 2D or 3D Specfiles can be written in one of three
languages: **JSON**, **YAML** and **TOML**. You have to indicated which one of them
was used by using either corresponding flag, *(\--yaml for YAML e.t.c)*
when using CLI or appropriate function *(render_from_yaml() for YAML e.t.c)*.

***************************
 Specfile for 2D rendering
***************************

Top level parameters
--------------------

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
         -  ``colors``, *optional*, see :ref:`usage/specfile:Defining Colors for layer`

Defining Colors for layer
-------------------------

``colors`` layer dictionary param can be omitted, then color will be
determined from Gerber file name. Chosen color will be one of
:ref:`usage/specfile:Predefined Colors` and first one which name will be
found in file name.

``colors`` can also be set to *string*, which have to be one of
:ref:`usage/specfile:Predefined Colors`.

Third option is to set colors manually via *dictionary*, then dictionary
has following keys, whose values ​​are lists of 3 or 4 integers in range
0-255 representing RGB / RGBA colors

   -  ``dark`` - *mandatory*, no default value
   -  ``clear`` - *optional*, defaults to transparent
   -  ``background`` *optional*, defaults to transparent

Predefined Colors
-----------------

Following predefined colors are defined:
   -  ``silk`` white, transparent, transparent
   -  ``paste_mask`` gray, transparent, transparent
   -  ``solder_mask`` light gray, transparent, transparent
   -  ``copper`` green, green (lighter), transparent
   -  ``orange`` orange, transparent, transparent
   -  ``green`` green, green (darker), transparent
   -  ``debug`` strange, strange, transparent

***************************
 Specfile for 3D rendering
***************************

