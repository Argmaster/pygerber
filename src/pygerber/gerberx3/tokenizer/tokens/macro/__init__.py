"""The AM command creates a macro aperture template and adds it to the aperture template
dictionary (see 2.2). A template is a parametrized shape. The AD command instantiates a
template into an aperture by supplying values to the template parameters.

Templates of any shape or parametrization can be created. Multiple simple shapes called
primitives can be combined in a single template. An aperture macro can contain variables
whose actual values are defined by:

- Values provided by the AD command

- Arithmetic expressions with other variables

The template is created by positioning primitives in a coordinate space. The origin of
that coordinate space will be the origin of all apertures created with the state.

A template must be defined before the first AD that refers to it. The AM command can be
used multiple times in a file.

Attributes are not attached to templates. They are attached to the aperture at the time
of its creation with the AD command.

An AM command contains the following words:

- The AM declaration with the macro name

- Primitives with their comma-separated parameters

- Macro variables, defined by an arithmetic expression
"""
