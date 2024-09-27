# Single file guide

This guide shows how to use `GerberFile` object from `pygerber.gerber.api` to to render
and format Gerber individual files. For overview of `pygerber.gerber.api` module,
including `GerberFile` construction options check out
[Introduction](./00_introduction.md). For guide on how to arrange multiple files into
single image using `Project` class check out
[Multi file project](./02_multi_file_project.md).

## Rendering Gerber file

`GerberFile` object exposes `render_with_pillow` method which renders Gerber file into
Pillow image object.

{{ include_code("test/examples/gerberx3/api/_00_single_file_render_with_pillow_defaults_str.example.py", "python", title="render_with_pillow.py", linenums="1") }}

`render_with_pillow()` method accepts `dpmm` parameter which can be used to set custom
dots-per-millimeter value, hence increase and decrease image resolution. By default this
value is set to 20, which is a safe default, but quite low for small PCBs.

`render_with_pillow()` returns `PillowImage` object which wraps actual image
(`PIL.Image.Image` object) and additional information about image coordinate space.

To retrieve image object, you can use `get_image()` method, then you can save it with
[`save()`](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save)
method offered by `PIL.Image.Image` object or transform with other methods. To find out
more please refer to [Pillow documentation](https://pillow.readthedocs.io/en/stable/).

To retrieve information about image space you can use `get_image_space()` method. This
method returns `ImageSpace` object which contains information about image coordinates,
image size, etc, as presented below:

{{ include_code("test/examples/gerberx3/api/_50_show_image_info.singlefile.py", "python", title="show_image_space.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/gerberx3/api/_50_show_image_info.singlefile.py", "python show_image_space.py") }}

## Formatting Gerber file

`GerberFile` object exposes `format()` and `formats()` methods which generate Gerber
code formatted according to the specified configuration. For detailed documentation of
formatting options, please refer to
[Formatter -> Configuration](../60_formatter/05_configuration.md).

The difference between `format()` and `formats()` methods is that `format()` method
writes formatted code to `TextIO`-like object while `formats()` returns it as a `str`
object.

{{ include_code("test/examples/gerberx3/api/_51_single_file_format.singlefile.py", "python", title="format_file.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/gerberx3/api/_51_single_file_format.singlefile.py", "python format_file.py") }}
