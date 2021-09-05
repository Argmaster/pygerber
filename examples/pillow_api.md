# 2D rendering API

### Rendering of single layer

Example of simplest possible manual rendering of Gerber file

```python
from pygerber import pillow

rendered_image = pillow.render_file("gerber/example_gerber.py")
rendered_image.show()
```

There is a shortcut for render and save

```python
from pygerber import pillow

pillow.render_and_save("./gerber/example_gerber.py", "example_gerber.png")
```

### Rendering of multiple layers

Rendering based on python dictionary, without configuration files

```python
from pygerber import pillow

# one image is returned - all layers stacked on top of each other
image = pillow.render_from_spec({
        "dpi": 600,
        "image_padding": 0,
        "ignore_deprecated": True,
        "layers": [
            {
                "file_path": ".\\gerber\\layers\\bottom.grb",
                "colors": {
                    "dark": [40, 143, 40, 255],
                    "clear": [60, 181, 60, 255],
                },
            },
            {
                "file_path": ".\\gerber\\layers\\top.grb",
                "colors": "silk",
            },
        ],
    })
image.show()
```

Rendering based on specification files written in **JSON**, **YAML** or **TOML** files

```python
from pygerber import pillow

# one image is returned - all layers stacked on top of each other
image = pillow.render_from_json("specfile.json")
image.show()
```

Example **JSON**, **YAML** and **TOML** files are available in [`tests/gerber/pillow/`](https://github.com/Argmaster/pygerber/blob/external-api/tests/gerber/pillow)
for more in-depth overview of specfile capabilities, see [`specfile.md`](https://github.com/Argmaster/pygerber/blob/external-api/examples/specfile.md)
