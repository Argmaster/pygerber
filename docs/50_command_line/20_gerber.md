# Gerber

Welcome to the Gerber focused part of PyGerber command line interface documentation.
This documentation is intended to show you how to use Gerber related command line tools
available in PyGerber.

## Image conversions

PyGerber offers a set of tools to convert Gerber files to raster and vector images. This
section will guide you through the process of converting Gerber files to images. All
supported image conversions can be listed with:

```bash
pygerber gerber convert --help
```

You can expect formats like PNG, JPEG and SVG to be present there.

!!! note

    SVG image format support requires a vector rendering engine, currently this means
    `shapely` extras set is required for SVG conversion to show up in the help.
    Preferably, you should use PyGerber extras set in case in future more dependencies
    will be required:

    ```bash
    pip install pygerber[shapely]
    ```

    You can also just install all optional extras with:

    ```bash
    pip install pygerber[all]
    ```

    This way you won't miss on any of the useful features.

Let's have look at an example of how one could convert a Gerber file to a PNG image:

```bash
pygerber gerber convert png "my_gerber_file.gbr" -o "output.png"
```

For raster images it is possible to include a `-d`/`--dpmm` parameter to alter the pixel
per millimeter density of output image. Default value can be too big for some PCBs and
to small for others, so keep in mind that it may be necessary to adjust it.

For vector images, you can convert Gerber files to SVG format:

```bash
pygerber gerber convert svg "my_gerber_file.gbr" -o "output.svg"
```

Technically each conversion command supports selection of implementation of the
rendering engine, but currently there is only one raster and one vector engine
available.

!!! note

    PyGerber is open for contributions, both regarding new output image formats as well as
    new rendering engines. If you have an idea for a new feature, feel free to open an
    issue on [GitHub](https://github.com/Argmaster/pygerber/issues/new/choose) or even
    better, submit a [pull request](https://github.com/Argmaster/pygerber/compare)!

## Formatting

PyGerber offers a tool to format Gerber files. This tool can be used to reformat Gerber
files to make them more readable or the opposite, to compress them to save precious disk
space. Technically, formatter includes also minor code modernization features although
less powerful than the Optimizer.

Let's have a look at an example of how one could format a Gerber file:

```bash
pygerber gerber format "my_gerber_file.gbr" -o "output.gbr"
```

Quite simple, isn't it? You can customize how file will be formatted (default settings
are really basic) by providing either inline configuration in JSON format or by using a
configuration file (also in JSON format).

Here is a simple example of how you could adjust indentation of macro bodies to 4
spaces:

```bash
pygerber gerber format src/pygerber/examples/carte_test-B_Cu.gbr -o formatted.gbr -i '{\"macro_body_indent\": 4}'
```

For more information about available configuration options, please refer to the
reference of `Options` class in
[here](../../reference/pygerber/gerber/formatter/options.md).
