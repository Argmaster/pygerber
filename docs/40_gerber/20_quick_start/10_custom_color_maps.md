# 🧁 Custom color maps

## Introduction

In PyGerber Gerber API (`pygerber.gerber.api` module) term color maps refers to
dictionaries used to convert type of layer (specified manually or determined
automatically) to style determining colors which should be used for rendering of that
layer.

Layer (file) type is expressed as `FileTypeEnum` value while style is expressed as
`Style` instance. Both classes are defined in `pygerber.gerber.api` module.

There are two predefined color maps in `pygerber.gerber.api`: `DEFAULT_COLOR_MAP` and
`DEFAULT_ALPHA_COLOR_MAP`. By default second one is used in `GerberFile` class during
rendering.

To create custom color map you need to create dictionary with keys being `FileTypeEnum`
values and values being `Style` instances. Then to change color map used by `GerberFile`
you need to call `set_color_map` method with your custom color map as argument.

## Single file example

{{ include_code("test/examples/gerberx3/api/_90_custom_color_map.example.py", "docspygerberlexer", title="custom_color_map.py", linenums="1") }}

## Multi file example

The reason for using dictionaries instead of just a parameter for render function is
that color map approach scales well for rendering multiple files from a project at once.
In such case colors will be automatically determined based on file types which can be
easily inferred from either file extension or file attributes.

See an example below:

{{ include_code("test/examples/gerberx3/api/_91_custom_color_map_project.example.py", "docspygerberlexer", title="custom_color_map_multi_file.py", linenums="1") }}

## Partial override

It might be tricky to guess all file types when rendering multiple files, especially if
we want to change colors only for single file type. In such case we can just copy
default color map which covers all file types and then override only colors for specific
file type.

{{ include_code("test/examples/gerberx3/api/_92_custom_color_map_partial_override.example.py", "docspygerberlexer", title="custom_color_map_multi_file.py", linenums="1") }}
