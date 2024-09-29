# Single file guide

This guide shows how to create and use `GerberFile` class instances to render and format
Gerber individual files. For guide on how to arrange multiple files into single image
using `Project` class check out [Multi file project](./02_multi_file_project.md).

`GerberFile` should be imported from `pygerber.gerber.api` module.

For full reference of `pygerber.gerber.api` module check out
[Reference](./20_pygerber_gerber_api_reference.md)

## Creating `GerberFile` object

{{ include_definition("pygerber.gerber.api.GerberFile", members="False", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

To perform any operations on Gerber file(s), like rendering or formatting, you have to
create
[`GerberFile`](./20_pygerber_gerber_api_reference.md#pygerber.gerber.api.GerberFile)
class instance wrapping actual Gerber code. Recommended way is to use one of 3 factory
methods provided by `GerberFile` class and listed below.

---

{{ include_definition("pygerber.gerber.api.GerberFile.from_str", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

To create `GerberFile` from `str` object you can use
[`GerberFile.from_str`](./20_pygerber_gerber_api_reference.md#pygerber.gerber.api.GerberFile.from_str)
factory method.

It accepts up to two arguments. First one is mandatory `source_code` which has to be a
Gerber code as `str` object. Second one is optional and can be used to manually set file
type (eg. silk screen, copper, drill etc.). If second argument is not provided, default
behavior is to try to guess file type based on file extension or file attributes. Method
returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_60_quick_start_from_str.quickstart.py", "python", title="example_from_str.py", linenums="1", hl_lines="12") }}

---

{{ include_definition("pygerber.gerber.api.GerberFile.from_file", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

Alternatively you can create `GerberFile` object from file using
[`GerberFile.from_file`](./20_pygerber_gerber_api_reference.md#pygerber.gerber.api.GerberFile.from_file)
factory method.

It accepts up to two arguments. First one is mandatory `file_path` which has to be a
path to existing file, either as `str` or `pathlib.Path` object. Second one is optional
and can be used to manually set file type (eg. silk screen, copper, drill etc.). If
second argument is not provided, default behavior is to try to guess file type based on
file extension or file attributes. Method returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_61_quick_start_from_file.quickstart.py", "python", title="example_from_file.py", linenums="1", hl_lines="6") }}

---

{{ include_definition("pygerber.gerber.api.GerberFile.from_buffer", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

Last way to create `GerberFile` object is to use
[`GerberFile.from_buffer`](./20_pygerber_gerber_api_reference.md#pygerber.gerber.api.GerberFile.from_buffer)
factory method.

It accepts up to two arguments. First one is mandatory `buffer` which has to be a
`TextIO`-like object supporting `read()` method. Second one is optional and can be used
to manually set file type (eg. silk screen, copper, drill etc.). If second argument is
not provided, default behavior is to try to guess file type based on file extension or
file attributes. Method returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_62_quick_start_from_buffer.quickstart.py", "python", title="example_from_buffer.py", linenums="1", hl_lines="5") }}

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

## Rendering Gerber file

{{ include_definition("pygerber.gerber.api.GerberFile.render_with_pillow", show_docstring_description="False ", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

[Reference](./20_pygerber_gerber_api_reference.md#pygerber.gerber.api.GerberFile.render_with_pillow)

`GerberFile` object exposes `render_with_pillow` method which renders Gerber file into
Pillow image object.

{{ include_code("test/examples/gerberx3/api/_00_single_file_render_with_pillow_defaults_str.example.py", "python", title="render_with_pillow.py", linenums="1") }}

`render_with_pillow()` method accepts `dpmm` parameter which can be used to set custom
dots-per-millimeter value, hence increase and decrease image resolution. By default this
value is set to 20, which is a safe default, but quite low for small PCBs.

`render_with_pillow()` returns `PillowImage` object which wraps actual image
(`PIL.Image.Image` object) and additional information about image coordinate space.

To retrieve image object, you can use `get_image()` method. Afterwards you can save it
with
[`save()`](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save)
method offered by `PIL.Image.Image` class instance or transform with other methods. To
find out more please refer to
[Pillow documentation](https://pillow.readthedocs.io/en/stable/).

To retrieve information about image space you can use `get_image_space()` method. This
method returns `ImageSpace` object which contains information about image coordinates,
image size, etc, as presented below:

{{ include_code("test/examples/gerberx3/api/_50_show_image_info.singlefile.py", "python", title="show_image_space.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/gerberx3/api/_50_show_image_info.singlefile.py", "python show_image_space.py") }}

## Formatting Gerber file

{{ include_definition("pygerber.gerber.api.GerberFile.format", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

{{ include_definition("pygerber.gerber.api.GerberFile.formats", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

`GerberFile` object exposes `format()` and `formats()` methods which generate Gerber
code formatted according to the specified configuration. For detailed documentation of
formatting options, please refer to
[Formatter -> Configuration](../60_formatter/10_configuration.md).

The difference between `format()` and `formats()` methods is that `format()` method
writes formatted code to `TextIO`-like object while `formats()` returns it as a `str`
object.

{{ include_code("test/examples/gerberx3/api/_51_single_file_format.singlefile.py", "python", title="format_file.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/gerberx3/api/_51_single_file_format.singlefile.py", "python format_file.py") }}
