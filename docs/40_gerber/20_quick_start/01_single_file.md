# Single file guide

Welcome to the PyGerber single file guide. This guide focuses on tools which take single
Gerber file as opposed to [Multi file guide](./02_multi_file.md) guide which is
concerned with operating on collections of Gerber files. Most of the functionality is
exposed as methods on `GerberFile` class which can be imported from
`pygerber.gerber.api` module and we will be using it throughout this document.

Currently `GerberFile` class provides means to render Gerber files into raster and
vector image formats and format Gerber code. Code optimization, cleanup and diagnostics
are on the roadmap.

## Creating `GerberFile` instance

To perform any operations on individual Gerber file(s), like rendering or formatting,
you have to create
[`GerberFile`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.GerberFile)
class instance wrapping actual Gerber code. Recommended way is to use one of 3 factory
methods provided by `GerberFile` class: `from_str()`, `from_file()` or `from_buffer()`

`from_str()` creates `GerberFile` from `str` object containing Gerber code.

{{ include_code("test/examples/gerberx3/api/_60_quick_start_from_str.quickstart.py", "docspygerberlexer", title="example_from_str.py", linenums="1", hl_lines="12") }}

`from_file()` creates `GerberFile` by reading a file which location is determined by
first parameter passed to `from_file()`. You can use `str` or `pathlib.Path` to specify
file location.

{{ include_code("test/examples/gerberx3/api/_61_quick_start_from_file.quickstart.py", "docspygerberlexer", title="example_from_file.py", linenums="1", hl_lines="6") }}

`from_buffer()` creates `GerberFile` from `io.TextIO`-like object.

{{ include_code("test/examples/gerberx3/api/_62_quick_start_from_buffer.quickstart.py", "docspygerberlexer", title="example_from_buffer.py", linenums="1", hl_lines="5") }}

Each of the factory methods listed above accept optional `file_type`
([`FileTypeEnum`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.FileTypeEnum)
)parameter which can be used to explicitly set file type (e.g. copper, silkscreen). If
this parameter is not set, by default PyGerber will try to guess file type based on file
extension and/or
[file attributes](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2022-02_en.pdf#page=125).

!!! info

    File type affects color of rendered image if color scheme is not explicitly set.

## Configuring `GerberFile` object

Once you have `GerberFile` object created, you can use PyGerber features exposed as
methods on this object. `GerberFile` allows you to customize behavior of some of
underlying implementation parts. Those methods mutate `GerberFile` object and
consecutive calls to those methods override previous configuration in its **entirety**.

[`set_color_map()`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.GerberFile.set_color_map)
can be used to override default color map.

Color map is used to map file type to predefined color style. PyGerber provides simple
color schema but it is useful mostly for final renders as colors used were chosen to
resemble final look of average PCB. Therefore you can easily provide your own color map.

Check out [Custom color maps](./10_custom_color_maps.md) for more details.

[`set_parser_options()`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.GerberFile.set_parser_options)
allows you to modify advanced parser settings. It is available to allow tweaking
predefined parser behavior options. If you need more control than provided here, please
check out [Extending Guide](../90_extend/00_introduction.md). `**options` are
intentionally not precisely defined here, as they are different for different parser
implementations, only way to use this method is to already understand what you are
doing.

[`set_compiler_options()`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.GerberFile.set_compiler_options)
allows you to modify advanced compiler settings. It is available to allow tweaking
predefined compiler behavior options. If you need more control than provided here,
please check out [Extending Guide](../90_extend/00_introduction.md). `**options` are
intentionally not precisely defined here, as they are different for different compiler
implementations, only way to use this method is to already understand what you are
doing.

## Rendering Gerber file

### Raster images

`GerberFile` object exposes
[`render_with_pillow()`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.GerberFile.render_with_pillow)
method which uses Gerber file renderer implemented with
[Pillow](https://pillow.readthedocs.io/en/stable) (Python Imaging Library (PIL) fork) to
generate raster images. Those images can be saved afterwards in PNG, JPEG etc. image
formats.

{{ include_code("test/examples/gerberx3/api/_00_single_file_render_with_pillow_defaults_str.example.py", "docspygerberlexer", title="render_with_pillow.py", linenums="1") }}

`render_with_pillow()` method accepts `dpmm` parameter which can be used to set custom
dots-per-millimeter value, hence increase and decrease image resolution. By default this
value is set to 20, which is a safe default, but quite low for small PCBs.

`render_with_pillow()` returns `PillowImage` object which wraps actual image
(`PIL.Image.Image` object) and additional information about image coordinate space.

<p align="center">
    <img src="single_file_pillow.png" alt="render_project" width="400" />
</p>

To retrieve image object, you can use `get_image()` method. Afterwards you can save it
with
[`save()`](https://pillow.readthedocs.io/en/stable/reference/Image.md#PIL.Image.Image.save)
method offered by `PIL.Image.Image` class instance or transform with other methods. To
find out more please refer to
[Pillow documentation](https://pillow.readthedocs.io/en/stable/).

To retrieve information about image space you can use `get_image_space()` method. This
method returns `ImageSpace` object which contains information about image coordinates,
image size, etc, as presented below:

{{ include_code("test/examples/gerberx3/api/_50_show_image_info.singlefile.py", "docspygerberlexer", title="show_image_space.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/gerberx3/api/_50_show_image_info.singlefile.py", "python show_image_space.py") }}

### Vector images

`GerberFile` object exposes
[`render_with_shapely()`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.GerberFile.render_with_shapely)
method which uses Gerber file renderer implemented with
[shapely](https://shapely.readthedocs.io/en/stable/manual.html) library to generate
vector images. Those images can be saved afterwards in SVG format.

`render_with_shapely()` returns `ShapelyImage` object which wraps output geometry and
additional information about image coordinate space. You can save the image in SVG
format using `save()` method

{{ include_code("test/examples/gerberx3/api/_05_single_file_render_with_shapely_defaults_file.example_svg.py", "docspygerberlexer", title="example.py", linenums="1") }}

<p align="center">
    <img src="single_file_shapely.svg" alt="render_project" width="400" />
</p>

!!! success "Improvements in PyGerber 3.0.0"

    In comparison to SVG rendering engine present in PyGerber 2.4.x,
    [shapely](https://shapely.readthedocs.io/en/stable/manual.html) based
    implementation performs actual boolean operations on geometry, therefore resulting in
    cleaner geometry which can be used to create 3D models, for example in blender.

### Image colors

There are three ways to change color of image created with `render_with_*()` methods.

First way is to explicitly pass `Style` instance as `style` parameter to
`render_with_*()` method. Style class offers predefined styles which can be accessed by
`Style.presets.<preset-name>`.

Second way is to change Gerber file type. File type can be deduced automatically but
also can be explicitly set in `GerberFile` factory method (`from_str`, `from_file`
etc.). File type will be mapped to specific `Style` based on color map.

Third way is to change what color map is used to convert file types to styles. This can
be achieved with `set_color_map()`, but for more details on how to specify custom color
maps see [Custom color maps](./10_custom_color_maps.md).

## Formatting Gerber file

`GerberFile` object exposes
[`format()`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.GerberFile.format)
and
[`formats()`](../../reference/pygerber/gerber/api/__init__.md#pygerber.gerber.api.GerberFile.formats)
methods which format Gerber code. For detailed documentation of formatting options,
please refer to [Formatter -> Configuration](../60_formatter/05_api_usage.md#).

The difference between `format()` and `formats()` methods is that first one writes
formatted code to `TextIO`-like object while second one returns it as a `str` object.

{{ include_code("test/examples/gerberx3/api/_51_single_file_format.singlefile.py", "docspygerberlexer", title="format_file.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/gerberx3/api/_51_single_file_format.singlefile.py", "python format_file.py", "gerber") }}

## Further reading

Check out full reference of
[`pygerber.gerber.api`](../../reference/pygerber/gerber/api/__init__.md).

For guide on how to arrange multiple files into single image using `Project` class check
out [Multi file project](./02_multi_file.md).
