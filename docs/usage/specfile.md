# Overview of specfiles capabilities

A specifle is a human-readable `JSON`, `YAML`, or `TOML` file containing rendering specifications. At the top level, it contains a dictionary with all keys except 'layers' being optional. Keys are always case-sensitive.

# Specfiles for 2D rendering with pillow

### Top level keys, that have impact on rendering are:

-   **dpi** - an integer specifying the DPI of the output image. Defaults to 600.

-   **ignore_deprecated** - if false, makes Gerber parser halt when it encounters deprecated syntax. Defaults to true.

-   **image_padding** - Adds additional image padding in both axes. Defaults to 0, meaning no padding.

-   **layers** - list of layers as dictionaries with keys described in **Layer dictionary keys for 2D rendering** chapter.

### Layer dictionary keys for 2D rendering:

-   **'file_path'** is mandatory, and contains a path to the Gerber file which should be rendered.

-   **'colors'** is optional and can contain:

    -   string with one of the predefined color names,
    -   dictionary with **dark** _(mandatory)_, **clear** _(optional)_, and **background** _(optional)_ keys, each containing a list of 3 or 4 integers representing **RGBA** color.

    If omitted, the parser will try to define a color set based on the filename. Names corresponding to predefined colors can be recognized.

### Available predefined colors are:

-   **silk** meaning 'dark' is white, 'clear' is transparent,
-   **paste_mask** meaning 'dark' is grey, 'clear' is transparent,
-   **solder_mask** meaning 'dark' is lighter grey, 'clear' is transparent,
-   **copper** meaning 'dark' is darker green, 'clear' is lighter green,

There are also few more, see [`pygerber/parser/pillow/api.py`](https://github.com/Argmaster/pygerber/blob/main/pygerber/parser/pillow/api.py#L20) **NAMED_COLORS** constant for details.

### Example specfile written in YAML

```yaml
dpi: 600
ignore_deprecated: yes
image_padding: 0
layers:
    - file_path: top_copper.grb
      colors:
          dark: [40, 143, 40, 255]
          clear: [60, 181, 60, 255]
    - file_path: top_solder_mask.grb
      colors: solder_mask
```

# Specfiles for 3D rendering with bpy (blender)

#### The following keys have an impact on how the image is rendered:

-   **layers** - list of layers as dictionaries with keys described in **Layer dictionary keys for 3D rendering** chapter.

### Layer dictionary keys for 2D rendering:

-   **'file_path'** is mandatory, and contains a path to the Gerber file which should be rendered.

-   **'structure'** is optional and can contain:

    -   string with one of the predefined structure names,
    -   dictionary with **color** _(mandatory)_, **thickness** _(mandatory)_. Color is a list of 3 or 4 integers either as RGB or RGBA

    If omitted, the parser will try to define structure based on the filename. Names corresponding to predefined structure can be recognized.