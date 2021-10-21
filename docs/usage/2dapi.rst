##################
 2D rendering API
##################

In general 2D rendering is faster and more reliable, as Gerber format
was not created with generating 3D models in mind. Therefore 2D
rendering was first one developed and currently has most extensive
support for Gerber language features.

**************************
 Single-file 2D rendering
**************************

Rendering single Gerber source file and saving it to a file can be done
the following way:

.. literalinclude:: ../../examples/pillow/render_file.py
   :language: python
   :caption: examples/pillow/render_file.py

Also, even though it takes only 2 lines of code, you can reduce it to
one function call:

.. literalinclude:: ../../examples/pillow/render_file_and_save.py
   :language: python
   :caption: examples/pillow/render_file_and_save.py

******************************
 Multi-file file 2D rendering
******************************

Rendering multiple files from one project is a bit more complicated as
it involves creating some sort of configuration, in form of a standalone
file or a dictionary generated on a fly.

Both files and dictionaries share data format and capabilities, which
you can learn more about from :ref:`usage/specfile:Specfile for 2D
rendering` chapter.

Example usage of dictionary configuration looks like this:

.. literalinclude:: ../../examples/pillow/render_from_spec.py
   :language: python
   :caption: examples/pillow/render_from_spec.py

As It was mentioned above, configuration can be also created in form of
standalone so called specfile, and then it can be used following way:

.. literalinclude:: ../../examples/pillow/render_from_yaml.py
   :language: python
   :caption: examples/pillow/render_from_yaml.py

And coresponding source of YAML specfile looks like this:

.. literalinclude:: ../../tests/gerber/pillow/specfile.yaml
   :language: python
   :caption: tests/gerber/pillow/specfile.yaml

Specfiles can be created using JSON, YAML and TOML however functions for
each one of the those languages differs only by function name suffix. We
have ``render_from_json`` for **JSON**, ``render_from_yaml`` for
**YAML** and ``render_from_toml`` for **TOML**, so there is no reason to
show separate examples for each.
