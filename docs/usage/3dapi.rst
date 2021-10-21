##################
 3D rendering API
##################

Generating 3D models from Gerber files is like generating C code from
compiled machine code. Its possible, can look cool when you look at it
from 3 meters distance, but it is a total mess when you try to analyze
it.

Therefore, don't expect generated 3D models to have great topology, or
be dragged and dropped into 3D printer to get some plastic showcase
model. (The later one can be achieved however, just requires some hand
tweaking, try `Remesh modifier` in blender)

They are mend for virtual showcase only, and they do their job pretty
well.

**************************
 Single-file 3D rendering
**************************

Similarly to 2D API, 3D API also contains ``render_file()`` function,
suitable for rendering standalone gerber files with minimal amount of
configuration:

.. literalinclude:: ../../examples/blender/render_file.py
   :language: python
   :caption: examples/blender/render_file.py

You can achieve same result as above code using `render_file_and_save()`
function:

.. literalinclude:: ../../examples/blender/render_file_and_save.py
   :language: python
   :caption: examples/blender/render_file_and_save.py

******************************
 Multi-file file 3D rendering
******************************

To render multiple files as one project you have to provide project
specification, which can be done using dictionary in code or standalone
config file written using JSON, YAML or TOML. Each specfile language has
its own separate render function, ``render_from_json()``,
``render_from_yaml()``, ``render_from_toml()``

Full explanation of configuration contents is described in
:ref:`usage/specfile:Specfile for 3D rendering` chapter.

Example usage of dictionary configuration looks like this:

.. literalinclude:: ../../examples/blender/render_from_spec.py
   :language: python
   :caption: examples/blender/render_from_spec.py

As It was mentioned above, configuration can be also created in form of
standalone so called specfile, and then it can be used following way:

.. literalinclude:: ../../examples/blender/render_from_yaml.py
   :language: python
   :caption: examples/blender/render_from_yaml.py

And coresponding source of YAML specfile looks like this:

.. literalinclude:: ../../tests/gerber/blender/specfile.yaml
   :language: python
   :caption: tests/gerber/blender/specfile.yaml
