<p align="center">
   <img width="400" src="https://github.com/Argmaster/pygerber/assets/56170852/b7aeb3e1-cd59-4f5b-b078-c01272461367" alt="" />
</p>

<h1 align="center"> PyGerber </h1>

<p align="center">
  <a href="https://github.com/Argmaster/pygerber/releases/"><img src="https://img.shields.io/github/v/release/Argmaster/pygerber?style=flat" alt="GitHub release"></a>
  <a href="https://github.com/Argmaster/pygerber/releases"><img src="https://img.shields.io/github/release-date/Argmaster/pygerber" alt="GitHub Release Date - Published_At"></a>
  <a href="https://pypi.org/project/pygerber"><img src="https://img.shields.io/pypi/v/pygerber?style=flat" alt="PyPI release"></a>
  <a href="https://pypi.org/project/pygerber/"><img src="https://img.shields.io/pypi/dm/pygerber.svg?label=PyPI%20downloads" alt="PyPI Downloads"></a>
  <a href="https://pypi.org/project/pygerber"><img src="https://img.shields.io/pypi/pyversions/pygerber?style=flat" alt="Supported Python versions"></a>
  <a href="https://pypi.org/project/pygerber"><img src="https://img.shields.io/pypi/implementation/pygerber?style=flat" alt="Supported Python implementations"></a>
  <a href="https://github.com/argmaster/pygerber/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Argmaster/pygerber" alt="license_mit"></a>
  <a href="https://codecov.io/gh/Argmaster/pygerber"><img src="https://codecov.io/gh/Argmaster/pygerber/branch/main/graph/badge.svg?token=VM09IHO13U" alt="coverage"></a>
  <a href="https://img.shields.io/github/checks-status/Argmaster/pygerber/main"><img src="https://img.shields.io/github/checks-status/Argmaster/pygerber/main" alt="GitHub tag checks state"></a>
  <a href="https://github.com/Argmaster/pygerber/pulls"><img src="https://img.shields.io/github/issues-pr/Argmaster/pygerber?style=flat" alt="Pull requests"></a>
  <a href="https://github.com/Argmaster/pygerber/issues"><img src="https://img.shields.io/github/issues-raw/Argmaster/pygerber?style=flat" alt="Open issues"></a>
  <a href="https://github.com/Argmaster/pygerber"><img src="https://img.shields.io/github/repo-size/Argmaster/pygerber" alt="GitHub repo size"></a>
  <a href="https://github.com/Argmaster/pygerber"><img src="https://img.shields.io/github/languages/code-size/Argmaster/pygerber" alt="GitHub code size in bytes"></a>
  <a href="https://github.com/Argmaster/pygerber"><img src="https://img.shields.io/github/stars/Argmaster/pygerber" alt="GitHub Repo stars"></a>
  <a href="https://python-poetry.org/"><img src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" alt="Poetry"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style"></a>
</p>

PyGerber is a Python implementation of Gerber X3/X2 format. It is based on Ucamco's
`The Gerber Layer Format Specification. Revision 2023.03` (Available on
[Ucamco's webpage](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-03_en.pdf)
and in
[this repository](https://github.com/Argmaster/pygerber/blob/main/docs/gerber_specification/gerber-layer-format-specification-revision-2023-03_en.pdf)).
The goal of this project is to provide support for wide variety of Gerber-like syntaxes,
with support for most of deprecated features along with support for modern ones.

<center><a href="https://argmaster.github.io/pygerber/latest"> 📚 See online documentation 📚 </a></center>

### Target set of tools:

- [x] Tokenizer
- [x] Parser
- [ ] Optimizer
- [x] [Introspection API](https://argmaster.github.io/pygerber/latest/gerber/introspection/0_usage.html)
- [x] Rasterized 2D rendering engine (With
      [Pillow](https://github.com/python-pillow/Pillow))
- [x] Vector 2D rendering engine (With [drawsvg](https://github.com/cduck/drawsvg))
- [ ] Model 3D rendering engine (With [Blender](https://www.blender.org/))
- [ ] Formatter
- [ ] Linter (eg. deprecated syntax detection)
- [x] Gerber X3/X2 Language Server (with `language-server` extras)

You can view progress of development in
[Gerber features support](#gerber-features-support) section down below. All Gerber
source files which can be redistributed under MIT license and included in this
repository for testing purposes will be greatly appreciated.

## Installation

PyGerber can be installed with `pip` from PyPI:

```
pip install pygerber
```

Alternatively, it is also possible to install it directly from repository:

```
pip install git+https://github.com/Argmaster/pygerber
```

### Language Server

Since release 2.1.0 PyGerber now provides Gerber X3/X2 Language Server with
[LSP](https://microsoft.github.io/language-server-protocol/) support. It can be enabled
by installing PyGerber extras set `language-server` with following command:

```
pip install pygerber[language-server]
```

Afterwards you can use `pygerber is-language-server-available` to check if language
server was correctly enabled. Please report all issues in
[PyGerber Issues](https://github.com/Argmaster/pygerber/issues) section.

## Command line usage

After installing `pygerber`, depending on your environment, it should become available
in your command line:

```bash
pygerber --version
```

Output should be similar to one below **⇩**, where `x.y.z` should match version of
PyGerber installed.

```
$ pygerber --version
pygerber, version x.y.z
```

Use `--help` to display help messages with lists of subcommands and subcommand options:

```
pygerber raster-2d --help
```

To render 2D PNG image of some gerber file you can simply use:

```
pygerber raster-2d gerber-source.grb
```

Image will be saved to `output.png` in current working directory.

![example_pcb_image](https://github.com/Argmaster/pygerber/assets/56170852/9bca28bf-8aa6-4215-aac1-62c386490485)

## Programmatic usage

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

### Advanced usage

Additionally to examples presented above which use high level API, PyGerber provides low
level API which allows to directly access PyGerber internals and change behavior of
parser, tokenizer and renderers. This can be used for code introspection and potentially
other purposed. Check out documentation for more information.

## Documentation

Official documentations is hosted on Github Pages and can be found
[here](https://argmaster.github.io/pygerber/latest).

## Gerber features support

Please refer to documentation for

- [Tokenizer](https://argmaster.github.io/pygerber/latest/gerber/feature_support/tokenizer.html),
- [Parser](https://argmaster.github.io/pygerber/latest/gerber/feature_support/parser.html),
- [Rasterized2DBackend](https://argmaster.github.io/pygerber/latest/gerber/feature_support/rasterized_2d.html),
- [Parser2](https://argmaster.github.io/pygerber/latest/gerber/feature_support/parser2.html),
- [SvgRenderer2](https://argmaster.github.io/pygerber/latest/gerber/feature_support/svgrenderer2.html),
- [RasterRenderer2](https://argmaster.github.io/pygerber/latest/gerber/feature_support/rasterrenderer2.html),

for detailed list of features which are supported/not supported by each tool.

## Syntax feature requests

All deprecated features (Mainly those from X2 format) are considered optional and
priority to implement them will be assigned based on number of requests form community.

If You needs support for syntax features which are not mentioned in
`The Gerber Layer Format Specification. Revision 2023.08` (Available on
[Ucamco's webpage](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf)
and in
[this repository](https://github.com/Argmaster/pygerber/blob/main/docs/gerber_specification/gerber-layer-format-specification-revision-2023-08_en.pdf))
and this feature is not already listed in Support paragraph, please open a new Feature
request issue.

**Feature request Issue should contain:**

- detailed description how requested feature works,
- code samples for testing the feature,
- reference images (only applies to features changing image look).

**Requests which don't comply with those guidelines will be considered low priority.**

## Development

To quickly set up development environment, first you have to install `poetry` globally:

```
pip install poetry
```

Afterwards you will be able to create development virtual environment:

```
poetry shell
```

Then You have to install dependencies into this environment:

```
poetry install
```

And pre-commit hooks:

```
poe install-hooks
```

Now you are good to go. Whenever you commit changes, pre-commit hooks will be invoked.
If they fail or change files, you will have to re-add changes and commit again.

## Build from source

To build PyGerber from source You have to set up [Development](#development) environment
first. Make sure you have `poetry` environment activated with:

```
poetry shell
```

With environment active it should be possible to build wheel and source distribution
with:

```
poetry build
```

Check `dist` directory within current working directory, `pygerber-x.y.z.tar.gz` and
`pygerber-x.y.z-py3-none-any.whl` should be there.

## Gerber reference archive

This repository contains also archival reference files. Although new specs contain
dedicated changelog section it may still be helpful in some rare cases to look through
old Gerber specs. Archival files can be found
[here](https://github.com/Argmaster/pygerber/tree/main/docs/gerber_specification).
