#######################
 PyGerber's Python API
#######################

PyGeber, despite having rather exhaustive command line interface, still
has some public functionalities that can be only accessed via Python
code.

Efforts have been made to ensure anything possible via CLI can be done
with similar ease in code, and we have impression that this goal was
achieved so far.

.. code:: text

   Important thing to mention before diving deeper into this part of documentation, is
   that you wont find here any description of internal API of PyGerber, nothing
   about parser, tokenizer and other internals. Documentation for such things
   has not been made, and the need for one has not been reported yet.

We will describe APIs for 2D and 3D rendering separately, even though in
CLI, they are pretty much identical and their APIs doesn't differ much
too, however they use different config file structure and are contained
in different files, therefore we decided to put emphasis on their
separateness.

.. toctree::

   2dapi
   3dapi
