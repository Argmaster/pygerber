# PyGerber

### PyGerber is a rendering engine for Gerber files.

PyGerber package provides API and CLI for `2D and 3D` rendering of Gerber files. We are using a `pillow` library for 2D and `Blender` for 3D rendering. We haven't implemented 3D rendering yet, but it's coming soon.


PyGerber for sure runs on`CPython 3.9.5.` No other versions have been tested.

#### API quick start example
```python
from python import pillow

image = pillow.render_file("example_gerber.py")
image.show()
```

For a complete overview of top-level 2D API usage, see `examples/pillow_api.md`

#### CLI quick start example
```bash
$ python -m pygerber --pillow --yamlspec "specfile.yaml"
```

For a complete overview of top-level CLI usage, see `examples/cli.md`



