# Overview of specfiles capabilities

A specifle is a human-readable `JSON`, `YAML`, or `TOML` file containing rendering specifications. At the top level, it contains a dictionary with all keys except 'layers' being optional. Keys are always case-sensitive.

#### The following keys have an impact on how the image is rendered:

-   **dpi** - an integer specifying the DPI of the output image. Defaults to 600.

-   **ignore_deprecated** - if false, makes Gerber parser halt when it encounters deprecated syntax. Defaults to true.

-   **image_padding** - Adds additional image padding in both axes. Defaults to 0, meaning no padding.

-   **layers** - list of layers - Gerber files - that will be stacked on top of each other. Defaults to an empty list and will cause an error when You try to render an empty list.

#### Each layer is a dictionary with two keys `'file_path'` and `'colors'`.

-   **'file_path'** is mandatory, and contains a path to the Gerber file which should be rendered.
-   **'colors'** is optional and can contain:
    * string with one of the predefined color names,
    * dictionary with **dark** *(mandatory)*, **clear** *(optional)*, and **background** *(optional)* keys, each containing a list of 3 or 4 integers representing **RGBA** color.

    If omitted, the parser will try to define a color set based on the filename. Names corresponding to predefined colors can be recognized.

#### Example specfile written in YAML

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

## Available colors are:
- *silk* meaning 'dark' is white, 'clear' is transparent,
- *paste_mask* meaning 'dark' is grey, 'clear' is transparent,
- *solder_mask* meaning 'dark' is lighter grey, 'clear' is transparent,
- *copper* meaning 'dark' is darker green, 'clear' is lighter green,

and a few more, see [`pygerber/parser/pillow/api.py`](https://github.com/Argmaster/pygerber/blob/external-api/pygerber/parser/pillow/api.py#L20) **NAMED_COLORS** constant for details.

