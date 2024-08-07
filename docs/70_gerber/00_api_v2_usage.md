# API Usage

## Hight Level API

### JPG

PyGerber can be used programmatically to render Gerber files. Below is an minimalistic
example of how to render one of the example files included with PyGerber release to JPEG
image:

```python
from pygerber.examples import ExamplesEnum, get_example_path
from pygerber.gerberx3.api.v2 import GerberFile

GerberFile.from_file(
    get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes),
).parse().render_raster("output.jpg")
```

Running code above will create `output.jpg` file in current working directory which
should look like this:

<p align="center">
  <img height="400" src="https://github.com/Argmaster/pygerber/assets/56170852/d17ebee8-e851-4c86-b110-8cd8aeca993e">
</p>

### PNG

It is also possible to render Gerber files to PNG with custom resolution and different
color schemes:

```python
from pygerber.examples import ExamplesEnum, get_example_path
from pygerber.gerberx3.api.v2 import ColorScheme, GerberFile, PixelFormatEnum

GerberFile.from_file(
    get_example_path(ExamplesEnum.ShapeFlashes),
).parse().render_raster(
    "output.png",
    dpmm=100,
    color_scheme=ColorScheme.COPPER_ALPHA,
    pixel_format=PixelFormatEnum.RGBA,
)
```

Code above renders following image:

<p align="center">
  <img height="400" src="https://github.com/Argmaster/pygerber/assets/56170852/0a5a42f3-8792-4b9a-be61-bac12f0e1c03">
</p>

### SVG

Finally you can also create SVG files with PyGerber:

```python
from pygerber.examples import ExamplesEnum, load_example
from pygerber.gerberx3.api.v2 import GerberFile

source_code = load_example(ExamplesEnum.UCAMCO_ex_2_Shapes)
GerberFile.from_str(source_code).parse().render_svg("output.svg")

```

### Multiple layers

PyGerber can also render multiple layers to single image. Below is an example of how to
render four layers to single PNG image with use of `Project` class:

```python
from pygerber.examples import ExamplesEnum, load_example
from pygerber.gerberx3.api.v2 import FileTypeEnum, GerberFile, Project

Project(
    [
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Cu),
            FileTypeEnum.COPPER,
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Mask),
            FileTypeEnum.MASK,
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Paste),
            FileTypeEnum.PASTE,
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Silkscreen),
            FileTypeEnum.SILK,
        ),
    ],
).parse().render_raster("output.png", dpmm=40)
```

Here is the result:

<p align="center">
  <img width="400" src="https://github.com/Argmaster/pygerber/assets/56170852/9b3f3823-67b3-49f1-8c76-e2bddaca81fe">
</p>

More detailed descriptions of interfaces can be found in
[API Reference](./01_api_v2_reference.md) page.

### Rendering with inferred color scheme

PyGerber can infer file type from file extension or `.FileFunction` file attribute.
Below is an simple example of how to render a file with inferred color scheme:

```python
from pygerber.gerberx3.api.v2 import GerberFile, DEFAULT_COLOR_MAP, FileTypeEnum

parsed_file = GerberFile.from_file(
    "test/assets/gerberx3/ATMEGA328-Motor-Board/ATMEGA328_Motor_Board-F.SilkS.gto",
    file_type=FileTypeEnum.INFER_FROM_EXTENSION
).parse()

color_scheme = DEFAULT_COLOR_MAP[parsed_file.get_file_type()]
parsed_file.render_raster("main.png", color_scheme=color_scheme)

```

Analogically, you can use `FileTypeEnum.INFER_FROM_ATTRIBUTES` to infer file type from
`.FileFunction` attribute.

!!! important

    `FileTypeEnum.INFER_FROM_EXTENSION` works only with `GerberFile.from_file()`.
    While using `GerberFile.from_str()` and `GerberFile.from_buffer()` no inference will
    be done resulting in `FileTypeEnum.UNDEFINED` file type.

If you want to automatically fall back from file extension inference to attribute based
inference, you can use `FileTypeEnum.INFER` file type. In such case if file extension
inference results in `FileTypeEnum.UNDEFINED`, PyGerber will try to infer file type from
`.FileFunction` attribute.
