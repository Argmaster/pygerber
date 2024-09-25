# Introduction

## Overview

This is a beginning of quick start guide for PyGerber. It uses a dedicated API which
exposes limited set of functionalities of PyGerber in very convenient way. It should
suite your needs if you are only looking for a quick way to render Gerber file(s) with
ability to choose basic options for parsing and rendering.

If you need to do something more complicated, you should check out **Advanced Guide** to
understand how PyGerber works and what can be achieved with its more complicated
interfaces.

## `pygerber.gerber.api` module

PyGerber exposes a simple API for accessing limited subset of its functionalities in
form of `pygerber.gerber.api` module. This interface is especially useful for one time
use, scripting and use from interactive shell. Most of the functionality has been
included in the `GerberFile` class and `Project` class. Additionally, there is a
`FileTypeEnum` containing recognized file types, few error classes and some less
important utility objects.

{{ pformat_variable("pygerber.gerber.api", "__all__") }}

## Creating `GerberFile` object

{{ include_definition("pygerber.gerber.api.GerberFile", members="False", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

To perform any operations on Gerber file(s), like rendering or formatting, you have to
create [`GerberFile`](./20_gerber_file.md#pygerber.gerber.api.GerberFile) object
wrapping actual Gerber code. Recommended way is to use one of 3 factory methods provided
by `GerberFile` class and listed below.

---

{{ include_definition("pygerber.gerber.api.GerberFile.from_str", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

To create `GerberFile` from `str` object you can use
[`GerberFile.from_str`](./20_gerber_file.md#pygerber.gerber.api.GerberFile.from_str)
factory method.

It accepts up to two arguments. First one is mandatory `source_code` which has to be a
Gerber code as `str` object. Second one is optional and can be used to manually set file
type (eg. silk screen, copper, drill etc.). If second argument is not provided, default
behavior is to try to guess file type based on file extension or file attributes. Method
returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_90_quick_start_from_str.py", "python", title="example_from_str.py", linenums="1", hl_lines="12") }}

---

{{ include_definition("pygerber.gerber.api.GerberFile.from_file", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

Alternatively you can create `GerberFile` object from file using
[`GerberFile.from_file`](./20_gerber_file.md#pygerber.gerber.api.GerberFile.from_file)
factory method.

It accepts up to two arguments. First one is mandatory `file_path` which has to be a
path to existing file, either as `str` or `pathlib.Path` object. Second one is optional
and can be used to manually set file type (eg. silk screen, copper, drill etc.). If
second argument is not provided, default behavior is to try to guess file type based on
file extension or file attributes. Method returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_91_quick_start_from_file.py", "python", title="example_from_file.py", linenums="1", hl_lines="6") }}

---

{{ include_definition("pygerber.gerber.api.GerberFile.from_buffer", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

Last way to create `GerberFile` object is to use
[`GerberFile.from_buffer`](./20_gerber_file.md#pygerber.gerber.api.GerberFile.from_buffer)
factory method.

It accepts up to two arguments. First one is mandatory `buffer` which has to be a
`TextIO`-like object supporting `read()` method. Second one is optional and can be used
to manually set file type (eg. silk screen, copper, drill etc.). If second argument is
not provided, default behavior is to try to guess file type based on file extension or
file attributes. Method returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_92_quick_start_from_buffer.py", "python", title="example_from_buffer.py", linenums="1", hl_lines="5") }}

---

## Configuring `GerberFile` object

Once you have `GerberFile` object created, you can use PyGerber features exposed as
methods on this object. `GerberFile` allows you to customize behavior of some of
underlying implementation parts. Those methods mutate `GerberFile` object and
consecutive calls to those methods override previous configuration in its **entirety**.

{{ include_definition("pygerber.gerber.api.GerberFile.set_parser_options", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

`set_parser_options` is a window into advanced parser settings, only reason to use this
method should be for advanced user to tweak parser behavior while using `GerberFile`
convenient API without binging more advanced PyGerber APIs into consideration.

{{ include_definition("pygerber.gerber.api.GerberFile.set_compiler_options", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

`set_compiler_options` is a window into advanced compiler settings, only reason to use
this method should be for advanced user to tweak compiler behavior while using
`GerberFile` convenient API without binging more advanced PyGerber APIs into
consideration.

{{ include_definition("pygerber.gerber.api.GerberFile.set_color_map", show_docstring_description="True", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

Color map is used to map file type to predefined color style. PyGerber provides simple
color schema but it is useful mostly for final renders as colors used were chosen to
resemble final look of average PCB. Therefore you can easily provide your own color map.

For detailed guide with examples on how to use those methods, please refer to the
[Single file guide](./01_single_file.md) section.

## Using `GerberFile` object

`GerberFile` exposes methods for transforming Gerber code into different code, images
etc., those meth are always produce new objects, they never mutate `GerberFile` object,
hence you can perform multiple operations using the same `GerberFile` object.

Available methods are:

{{ include_definition("pygerber.gerber.api.GerberFile.render_with_pillow", show_docstring_description="True", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

[Reference](./20_gerber_file.md#pygerber.gerber.api.GerberFile.render_with_pillow)

{{ include_definition("pygerber.gerber.api.GerberFile.format", show_docstring_description="True", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

[Reference](./20_gerber_file.md#pygerber.gerber.api.GerberFile.format)

{{ include_definition("pygerber.gerber.api.GerberFile.formats", show_docstring_description="True", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

[Reference](./20_gerber_file.md#pygerber.gerber.api.GerberFile.formats)

For detailed guide with examples on how to use those methods, please refer to the
[Single file guide](./01_single_file.md) section.

## Arranging multiple files

{{ include_definition("pygerber.gerber.api.Project", members="False", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

To arrange multiple files into single image you can use `Project` class. It is a simple
wrapper around multiple `GerberFile` objects. It automatically aligns all images and
determines how big final image has to be to fit all images and merges them into single
image. It is still possible to retrieve individual images from result returned by
rendering methods.

For detailed guide with examples on how to use `Project` class, please refer to the
[Multi file project](./02_multi_file_project.md) section.
