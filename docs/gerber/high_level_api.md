# High Level API

PyGerber offers simple high-level API for rendering Gerber files. All necessary tools
can be imported from `pygerber.gerberx3.api` module. See
[module reference](../reference/pygerber/gerberx3/api/__init__.md) for full object list.

!!! important

    API of `pygerber.gerberx3.api` module is guaranteed to remain unchanged between
    patches and minor releases of PyGerber, whereas other modules, even those contained
    deeper in `pygerber.gerberx3.api` like `gerber.gerberx3.api._layers`, may change at
    any time.

!!! bug

    [Please report](https://github.com/Argmaster/pygerber/issues/new) any objects which
    have to be imported from other places than `pygerber.gerberx3.api` for high level
    API, it's typechecking or error handling to work. Such situations are considered a
    bug.

## Overview

- `Layer` class and it's subclasses in PyGerber API represent a Gerber file. It's
  completely different meaning than in PCB design, much closer to what a image layer is
  in image manipulation software, like [Gimp](https://www.gimp.org/). `Layer` class
  itself it not a functional, only it's subclasses can be used to instruct PyGerber how
  to render Gerber file. Based on what `Layer` subclass is used, different output image
  types can be obtained. For example `Rasterized2DLayer` will allow for generating
  rasterized images and saving them as JPEG, PNG, TIFF and other image formats.

- `LayerParams` class and its subclasses are intended to be used to configure the
  corresponding `Layer` classes. For example, when using `Rasterized2DLayer` for
  rendering, it is only valid to pass `Rasterized2DLayerParams` to constructor. Passing
  incorrect `LayerParams` subclass will result in `TypeError`.

- `RenderingResult` class is returned from `render()` method of `Layer` instance. It
  provides simple interface for saving rendering output. Different output formats will
  be available depending on the layer type used. For `Rasterized2DLayer` list of
  supported output formats is equivalent to list of formats supported by Pillow library.
  It can be found in
  [Pillow documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

## Usage

Below we provided an example of simple API use.

We have following Gerber file:

```gerber linenums="1" title="render_copper_from_path.grb"
{% include 'test/examples/render_copper_from_path.grb' %}
```

Which should result in simple image:

![render_copper_from_path](https://github.com/Argmaster/pygerber/assets/56170852/368da7e3-36ae-42ec-bbd2-f1c296b6b42d)

To achieve such result with PyGerber, first we have to import all necessary classes from
`pygerber.gerberx3.api` module:

```py linenums="1"
from pygerber.gerberx3.api import (
    ColorScheme,
    Rasterized2DLayer,
    Rasterized2DLayerParams,
)
```

We will be using `Rasterized2DLayer`, as we want to create a PNG image.
`Rasterized2DLayerParams` will be necessary to specify path to source file and image
color scheme, declared with `ColorScheme`:

```py linenums="6"
options = Rasterized2DLayerParams(
    source_path="render_copper_from_path.grb",
    colors=ColorScheme.COPPER_ALPHA,
)
```

!!! example "`ColorScheme` creation."

    `ColorScheme.COPPER_ALPHA` is a predefined color scheme, equivalent can be created
    manually:

    ```py
    ColorScheme.COPPER_ALPHA = ColorScheme(
        background_color=RGBA.from_rgba(0, 0, 0, 0),
        clear_color=RGBA.from_rgba(60, 181, 60, 255),
        solid_color=RGBA.from_rgba(40, 143, 40, 255),
        clear_region_color=RGBA.from_rgba(60, 181, 60, 255),
        solid_region_color=RGBA.from_rgba(40, 143, 40, 255),
    )
    ```

    See reference for all possible ways of creating
    [`RGBA` color objects](../reference/pygerber/gerberx3/api/__init__.md#pygerber.gerberx3.api.RGBA)
    and [`ColorSchema` color schema objects](../reference/pygerber/gerberx3/api/__init__.md#pygerber.gerberx3.api.ColorScheme).

Afterwards we can create a `Rasterized2DLayer` object. Remember to provide previously
constructed `Rasterized2DLayerParams` instance to constructor:

```py linenums="10"
layer = Rasterized2DLayer(options=options)
```

Now we can use `render()` method of `Rasterized2DLayer` instance to create
`RenderingResult`:

```py linenums="11"
result = layer.render()
```

Then we can call `save()` method on `RenderingResult` to save rendered image to drive:

```py linenums="12"
result = layer.save("output.png")
```

Alternatively you can save image to BytesIO:

```py linenums="13"
from io import BytesIO
buffer = BytesIO()
result = layer.save(buffer, format="PNG)
```

## More examples

Below are few more examples showing how to provide Gerber code to `Layer` by different
ways, however they are all equivalent.

### Load from file path

```py linenums="1" title="test/examples/render_copper_from_path.py"
{% include 'test/examples/render_copper_from_path.py' %}
```

---

### Read from buffer

```py linenums="1" title="test/examples/render_copper_from_buffer.py"
{% include 'test/examples/render_copper_from_buffer.py' %}
```

---

### Read from string

```py linenums="1" title="test/examples/render_copper_from_string.py"
{% include 'test/examples/render_copper_from_string.py' %}
```

---

## Obtaining layer properties

I some cases it may be useful to obtain information about layer which was rendered. For
example origin of coordinate system of image can be useful for aligning multiple layers
on top of each other, or for other similar transformations.

Those information can be extracted from `RenderingResult` object, returned from
`Layer.render()` method. `RenderingResult` object has `get_properties()` method which
returns `LayerProperties` object which contains all the necessary data to determine
coordinate origins and bounding boxes of layer.

## Further reading

To further extend your knowledge about how to use PyGerber you could read
[`pygerber.gerberx3.api` module reference](../reference/pygerber/gerberx3/api/__init__.md)
or see [Gerber Advanced API]("gerber_advanced_api.md")

---
