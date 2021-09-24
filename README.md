# PyGerber

### PyGerber is a tool for parsing and rendering Gerber files

PyGerber offers a CLI and API for Python to allow easy rendering of Gerber files. It was build with GBR X3 format in mind. However, it has extensive support for older standards.
External libraries are used for low-level drawing operations: [pillow](https://python-pillow.org/) for `2D` rendering and [bpy](https://www.blender.org/) (blender) for `3D` rendering.

`3D rendering is still under development, it will arrive at next major release.`

PyGerber for sure runs on`CPython 3.9.5`. No other versions have been tested. 3D rendering is most likely to be available only for this version due to blenders compatibility.

## Installation

You can install PyGerber from PyPI using pip:

```bash
$ pip install pygerber
```

### API quick start example

Even tho PyGerber has complicated internal structure, most likely it will be enough for You to use simplified public API,
as shown below. Pillow submodule is responsible for 2D rendering.

```python
from pygerber import pillow

image = pillow.render_file("example_gerber.py")
image.show()
```

For a complete overview of top-level 2D API usage, see [`examples/pillow_api.md`](https://github.com/Argmaster/pygerber/blob/main/examples/2d_api.md)

### CLI quick start example

CLI has a similar set of capabilities to the API, allowing you to render both single layers and multilayer projects using the command line.

_Note that unlike the API, CLI has a shared interface for both 2D and 3D rendering_

```bash
$ python -m pygerber --pillow --yaml "specfile.yaml" -s "render.png"
```

For a complete overview of top-level CLI usage, see [`examples/cli.md`](https://github.com/Argmaster/pygerber/blob/main/examples/cli.md)
