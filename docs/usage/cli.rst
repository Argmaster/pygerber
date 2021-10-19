########################
 Command Line Interface
########################

First and foremost, the PyGerber command line help page can be displayed
with this command:

.. code:: bash

   $ python -m pygerber -h

**********************
 2D rendering Example
**********************

To render project in 2D, specified by
"tests/gerber/pillow/specfile.yaml" (from our repo) and save it as PNG
named "render.png" we can use following command:

.. code:: bash

   $ python -m pygerber --pillow --toml "tests/gerber/pillow/specfile.yaml" -s "render.png"

YAML specfile used defines simple 4-layer PCB project and looks like
this:

.. literalinclude:: ../../tests/gerber/pillow/specfile.yaml
   :language: yaml
   :caption: tests/gerber/pillow/specfile.yaml

On the very top level it specifies **DPI** of output image, **600** in
our case, and sets **image padding** to **no padding**. Then **layers**
param specifies layers from bottom-most to top-most. You have to at
least specify path to gerber file in layer. For more about specfiles see
:ref:`usage/specfile:Specfile for 2D rendering` chapter.

**********************
 3D rendering Example
**********************

3D rendering works identically, except that specfiles have a slightly
different set of parameters. Again, see :ref:`usage/specfile:Specfile
for 3D rendering` chapter for more in-depth description. (DRY :D )

We also have example specfiles for 3D rendering in our repo, lets see
how to use them

.. code:: bash

   $ python -m pygerber --blender --toml "tests/gerber/blender/specfile.json" -s "render.glb"

That's exactly the same 4 layer project, only this time in 3D and with
specfile written in JSON instead of YAML

.. literalinclude:: ../../tests/gerber/blender/specfile.json
   :language: json
   :caption: tests/gerber/blender/specfile.json

As You can see, both top level options and layer specifications differ a
bit, but remain similar. For the third time, I insist that you visit
:ref:`usage/specfile:Specfile for 3D rendering`. If you did, you should
already be aware of the meaning of this file's structure.
