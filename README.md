<p align="center">
  <img width="400" src="https://github.com/Argmaster/pygerber/assets/56170852/b7aeb3e1-cd59-4f5b-b078-c01272461367">
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

### Target set of tools:

- [x] Tokenizer
- [x] Parser
- [ ] Optimizer
- [x] Rasterized 2D rendering engine (With
      [Pillow](https://github.com/python-pillow/Pillow))
- [ ] Vector 2D rendering engine (With [drawsvg](https://github.com/cduck/drawsvg))
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

## API usage

PyGerber offers a high-level API that simplifies the process of rendering Gerber files.
Whether you're looking to save the rendered output to a file or directly into a buffer,
PyGerber has got you covered.

- **The `Layer` Class**: At its core, the `Layer` class stands for a single Gerber
  source file, complete with its associated PyGerber configuration.

  **Important** `Layer` class represents **any** Gerber file, **not** layer of PCB. For
  example, silkscreen Gerber file will require one instance of `Layer`, paste mask will
  require another one, copper top yet another, etc.

- **Configuration Flexibility**: The configuration possibilities you get with a `Layer`
  are driven by the backend you choose to render your source file.

- **Selecting a Backend**: PyGerber provides specialized subclasses of the `Layer` class
  each tied to one rendering backend. For instance, if you're aiming for 2D rasterized
  images, `Rasterized2DLayer` is your go-to choice.

- **Output Types**: Keep in mind, the type of your output file is closely tied to the
  backend you select.For 2D rasterized rendering
  [all formats supported by Pillow](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)
  are accepted.

### Rasterized render from file

```py linenums="1" title="render_file.py"
from pygerber.gerberx3.api import (
      ColorScheme,
      Rasterized2DLayer,
      Rasterized2DLayerParams,
)

# Path to Gerber source file.
source_path = "main_cu.grb"

Rasterized2DLayer(
      options=Rasterized2DLayerParams(
            source_path=source_path,
            colors=ColorScheme.COPPER_ALPHA,
      ),
).render().save("output.png")
```

Example code above creates `Rasterized2DLayer` object, renders it with rasterized 2D
backend and saves it as `PNG` image. Use of `Rasterized2DLayer` and
`Rasterized2DLayerOptions` classes implicitly use 2D rasterized backend. To use
different rendering backend with high level API, user must pick different `Layer` and
`LayerOptions` subclasses. For other backends see
[Target set of tools](#target-set-of-tools) section, note that only checked ones are
available.

`source_path` option accepts `str` or `Path` pointing to local Gerber file. No special
file extension is required, content is blindly loaded from specified file, so it's user
responsibility to provide correct path. There are also `source_code` and `source_buffer`
parameters which allow for use of raw `str` or `bytes` objects (first one) and
`StringIO` and `BytesIO` or file descriptors (second one). `source_code`,
`source_buffer` and `source_path` are mutually exclusive.

`ColorScheme` is a class which describes what colors should be used for rendering
different parts of image. Additionally it has a few static members which contain
predefined colors schemes for frequently used layer types. It is not required to use
predefined schemes, creating and passing custom `ColorScheme` object should work
perfectly fine.

Pattern of using `<Class>` and `<Class>Options`, like above, is used in many places in
PyGerber. When initializing object like `Rasterized2DLayer` it is only valid to pass
`Rasterized2DLayerOptions` to constructor. Passing `LayerOptions` or `Vectorized2DLayer`
will cause undefined behavior, most likely yielding no result or raising exception.

### Rasterized render from string

```py linenums="1" title="render_string.py"
from pygerber.gerberx3.api import (
      ColorScheme,
      Rasterized2DLayer,
      Rasterized2DLayerParams,
)

source_code = """
%FSLAX26Y26*%
%MOMM*%
%ADD100R,1.5X1.0X0.5*%
%ADD200C,1.5X1.0*%
%ADD300O,1.5X1.0X0.6*%
%ADD400P,1.5X3X5.0*%
D100*
X0Y0D03*
D200*
X0Y2000000D03*
D300*
X2000000Y0D03*
D400*
X2000000Y2000000D03*
M02*
"""

Rasterized2DLayer(
      options=Rasterized2DLayerParams(
            source_code=source_code,
            colors=ColorScheme.SILK,
            dpi=3000,
      ),
).render().save("output.png")

```

Code above renders following image:

<p align="center">
  <img width="414" height="384" src="https://github.com/Argmaster/pygerber/assets/56170852/56b6757b-0f97-4a18-9d43-f21711c71c71">
</p>

## Documentation

Official documentations is hosted on Github Pages and can be found
[here](https://argmaster.github.io/pygerber/).

## Gerber features support

This section outlines the support for various Gerber format features in PyGerber's core
components: [**Tokenizer**](#tokenizer), [**Parser**](#parser), and
[**Rasterized2DBackend**](#rasterized2dbackend). We use checkboxes to indicate which
features are currently implemented. Checked boxes represent supported features, while
unchecked boxes denote features still under development or not available.

### Tokenizer

Supported Gerber X3 features:

- [x] G04 - Comment - A human readable comment, does not affect the image.
- [x] MO - Mode - Sets the unit to mm or inch.
- [x] FS - Format specification - Sets the coordinate format, e.g. the number of
      decimals.
- [x] FS (Deprecated modes)
- [x] AD - Aperture define - Defines a template-based aperture, assigns a D code to it.
- [x] AM - Aperture macro - Defines a macro aperture template.
- [x] Dnn (nn≥10) - Sets the current aperture to D code nn.
- [x] D01 - Plot operation - Outside a region statement D01 creates a draw or arc object
      with the current aperture. Inside it adds a draw/arc segment to the contour under
      construction. The current point is moved to draw/arc end point after the creation
      of the draw/arc.
- [x] D02 - Move operation - D02 moves the current point to the coordinate in the
      command. It does not create an object.
- [x] D03 - Flash operation - Creates a flash object with the current aperture. The
      current point is moved to the flash point.
- [x] G01 - Sets linear/circular mode to linear.
- [x] G02 - Sets linear/circular mode to clockwise circular.
- [x] G03 - Sets linear/circular mode to counterclockwise circular.
- [x] G75 - A G75 must be called before creating the first arc.
- [x] LP - Load polarity - Loads the polarity object transformation parameter.
- [x] LM - Load mirroring - Loads the mirror object transformation parameter.
- [x] LR - Load rotation - Loads the rotation object transformation parameter.
- [x] LS - Load scaling - Loads the scale object transformation parameter.
- [x] G36 - Starts a region statement which creates a region by defining its contours.
- [x] G37 - Ends the region statement.
- [x] AB - Aperture block - Opens a block aperture statement and assigns its aperture
      number or closes a block aperture statement.
- [x] SR - Step and repeat - Open or closes a step and repeat statement.
- [x] TF - Attribute on file - Set a file attribute.
- [x] TA - Attribute on aperture - Add an aperture attribute to the dictionary or modify
      it.
- [x] TO - Attribute on object - Add an object attribute to the dictionary or modify it.
- [x] TD - Attribute delete - Delete one or all attributes in the dictionary.
- [x] M02 - End of file.

Supported **DEPRECATED** Gerber features:

- [x] G54 - Select aperture - This historic code optionally precedes an aperture
      selection Dnn command. It has no effect. Sometimes used. Deprecated in 2012.
- [ ] G55 - Prepare for flash - This historic code optionally precedes D03 code. It has
      no effect. Very rarely used nowadays. Deprecated in 2012.
- [x] G70 - Set the 'Unit' to inch - These historic codes perform a function handled by
      the MO command. See 4.2.1. Sometimes used. Deprecated in 2012.
- [x] G71 - Set the 'Unit' to mm - This is part of the historic codes that perform a
      function handled by the MO command.
- [x] G90 - Set the 'Coordinate format' to 'Absolute notation' - These historic codes
      perform a function handled by the FS command. Very rarely used nowadays.
      Deprecated in 2012.
- [x] G91 - Set the 'Coordinate format' to 'Incremental notation' - Part of the historic
      codes handled by the FS command.

  - **Important**: _Incremental notation itself is not supported and is not planned due
    to lack of test assets and expected complications during implementation._

- [x] G74 - Sets single quadrant mode - Rarely used, and then typically without effect.
      Deprecated in 2020. (Spec. 8.1.10)
- [x] M00 - Program stop - This historic code has the same effect as M02. Very rarely,
      if ever, used nowadays. Deprecated in 2012.
- [x] M01 - Optional stop - This historic code has no effect. Very rarely, if ever, used
      nowadays. Deprecated in 2012.
- [x] IP - Sets the 'Image polarity' graphics state parameter - This command has no
      effect in CAD to CAM workflows. Sometimes used, and then usually as %IPPOS\*% to
      confirm the default and then it then has no effect. Deprecated in 2013. (Spec.
      8.1.4)
- [ ] AS - Sets the 'Axes correspondence' graphics state parameter - Deprecated in 2013.
      Rarely used nowadays. (Spec. 8.1.2)
- [ ] IR - Sets 'Image rotation' graphics state parameter - Deprecated in 2013. Rarely
      used nowadays. (Spec. 8.1.5)
- [ ] MI - Sets 'Image mirroring' graphics state parameter (Spec. 8.1.7)
- [ ] OF - Sets 'Image offset' graphics state parameter (Spec. 8.1.8)
- [ ] SF - Sets 'Scale factor' graphics state parameter (Spec. 8.1.9)
- [ ] IN - Sets the name of the file image. Has no effect. It is comment. Sometimes
      used. Deprecated in 2013. (Spec. 8.1.3)
- [x] LN - Loads a name. Has no effect. It is a comment. Sometimes used. Deprecated
      in 2013. (Spec. 8.1.6)
- [x] Combining G01/G02/G03 and D01 in a single command. (Spec 8.3.1)
- [x] Coordinate Data without Operation Code. (Spec 8.3.2)
- [x] Style Variations in Command Codes. (Spec 8.3.3)
- [ ] Deprecated usage of SR. (Spec 8.3.4)
- [ ] Deprecated Attribute Values. (Spec 8.4)
- [x] Format Specification (FS) Options (Trailing Zero Omission, Incremental Notation).
      (Spec. 8.2)

  - **Important**: _Incremental notation itself is not supported and is not planned due
    to lack of test assets and expected complications during implementation._

- [ ] Rectangular Hole in Standard Apertures (Spec. 8.2.2)
- [x] Draws and Arcs with Rectangular Apertures (Spec. 8.2.3)
- [ ] Macro Primitive Code 2, Vector Line (Spec. 8.2.4)
- [ ] Macro Primitive Code 22, Lower Left Line (Spec. 8.2.5)
- [ ] Macro Primitive Code 6, Moiré (Spec. 8.2.6)

### Parser

Supported Gerber X3 features:

- [x] MO - Mode - Sets the unit to mm or inch.
- [x] FS - Format specification - Sets the coordinate format, e.g. the number of
      decimals.
- [ ] AD - Aperture define - Defines a template-based aperture, assigns a D code to it.
  - [x] Define circle.
  - [x] Define rectangle.
  - [x] Define obround.
  - [x] Define polygon.
  - [ ] Define macro.
- [ ] AM - Aperture macro - Defines a macro aperture template.
- [x] Dnn (nn≥10) - Sets the current aperture to D code nn.
- [x] D01 - Plot operation - Outside a region statement D01 creates a draw or arc object
      with the current aperture.
- [x] D01 - Plot operation - Inside region statement adds a draw/arc segment to the
      contour under construction. The current point is moved to draw/arc end point after
      the creation of the draw/arc.
- [x] D02 - Move operation - D02 moves the current point to the coordinate in the
      command. It does not create an object.
- [x] D03 - Flash operation - Creates a flash object with the current aperture. The
      current point is moved to the flash point.
- [x] G01 - Sets linear/circular mode to linear.
- [x] G02 - Sets linear/circular mode to clockwise circular.
- [x] G03 - Sets linear/circular mode to counterclockwise circular.
- [x] LP - Load polarity - Loads the polarity object transformation parameter.
- [x] LM - Load mirroring - Loads the mirror object transformation parameter.
- [x] LR - Load rotation - Loads the rotation object transformation parameter.
- [x] LS - Load scaling - Loads the scale object transformation parameter.
- [x] G36 - Starts a region statement which creates a region by defining its contours.
- [x] G37 - Ends the region statement.
- [ ] AB - Aperture block - Opens a block aperture statement and assigns its aperture
      number or closes a block aperture statement.
- [ ] SR - Step and repeat - Open or closes a step and repeat statement.
- [ ] TF - Attribute on file - Set a file attribute.
- [ ] TA - Attribute on aperture - Add an aperture attribute to the dictionary or modify
      it.
- [ ] TO - Attribute on object - Add an object attribute to the dictionary or modify it.
- [ ] TD - Attribute delete - Delete one or all attributes in the dictionary.
- [x] M02 - End of file.

Supported **DEPRECATED** Gerber features:

- [x] G54 - Select aperture - This historic code optionally precedes an aperture
      selection Dnn command. It has no effect. Sometimes used. Deprecated in 2012.
- [ ] G55 - Prepare for flash - This historic code optionally precedes D03 code. It has
      no effect. Very rarely used nowadays. Deprecated in 2012.
- [x] G70 - Set the 'Unit' to inch - These historic codes perform a function handled by
      the MO command. See 4.2.1. Sometimes used. Deprecated in 2012.
- [x] G71 - Set the 'Unit' to mm - This is part of the historic codes that perform a
      function handled by the MO command.
- [x] G90 - Set the 'Coordinate format' to 'Absolute notation' - These historic codes
      perform a function handled by the FS command. Very rarely used nowadays.
      Deprecated in 2012.
- [x] G91 - Set the 'Coordinate format' to 'Incremental notation' - Part of the historic
      codes handled by the FS command.

  - **Important**: _Incremental notation itself is not supported and is not planned due
    to lack of test assets and expected complications during implementation._

- [x] G74 - Sets single quadrant mode - Rarely used, and then typically without effect.
      Deprecated in 2020. (Spec. 8.1.10)
- [x] M00 - Program stop - This historic code has the same effect as M02. Very rarely,
      if ever, used nowadays. Deprecated in 2012.
- [x] M01 - Optional stop - This historic code has no effect. Very rarely, if ever, used
      nowadays. Deprecated in 2012.
- [x] IP - Sets the 'Image polarity' graphics state parameter - This command has no
      effect in CAD to CAM workflows. Sometimes used, and then usually as %IPPOS\*% to
      confirm the default and then it then has no effect. Deprecated in 2013. (Spec.
      8.1.4)
- [ ] AS - Sets the 'Axes correspondence' graphics state parameter - Deprecated in 2013.
      Rarely used nowadays. (Spec. 8.1.2)
- [ ] IR - Sets 'Image rotation' graphics state parameter - Deprecated in 2013. Rarely
      used nowadays. (Spec. 8.1.5)
- [ ] MI - Sets 'Image mirroring' graphics state parameter (Spec. 8.1.7)
- [ ] OF - Sets 'Image offset' graphics state parameter (Spec. 8.1.8)
- [ ] SF - Sets 'Scale factor' graphics state parameter (Spec. 8.1.9)
- [ ] IN - Sets the name of the file image. Has no effect. It is comment. Sometimes
      used. Deprecated in 2013. (Spec. 8.1.3)
- [x] LN - Loads a name. Has no effect. It is a comment. Sometimes used. Deprecated
      in 2013. (Spec. 8.1.6)
- [x] Combining G01/G02/G03/G70/G71 and D01 in a single command. (Spec 8.3.1)
- [x] Combining G01/G02/G03/G70/G71 and D02 in a single command.
- [x] Combining G01/G02/G03/G70/G71 and D03 in a single command.
- [x] Coordinate Data without Operation Code. (Spec 8.3.2)
- [x] Style Variations in Command Codes. (Spec 8.3.3)
- [ ] Deprecated usage of SR. (Spec 8.3.4)
- [ ] Deprecated Attribute Values. (Spec 8.4)
- [ ] Format Specification (FS) Options (Trailing Zero Omission, Incremental Notation).
      (Spec. 8.2)

  - **Important**: _Incremental notation itself is not supported and is not planned due
    to lack of test assets and expected complications during implementation._

- [ ] Rectangular Hole in Standard Apertures (Spec. 8.2.2)
- [ ] Draws and Arcs with Rectangular Apertures (Spec. 8.2.3)
- [ ] Macro Primitive Code 2, Vector Line (Spec. 8.2.4)
- [ ] Macro Primitive Code 22, Lower Left Line (Spec. 8.2.5)
- [ ] Macro Primitive Code 6, Moiré (Spec. 8.2.6)

### Rasterized2DBackend

Supported Gerber X3 features:

- [x] Aperture definition with circle
- [x] Aperture definition with rectangle
- [x] Aperture definition with obround
- [x] Aperture definition with polygon
- [ ] Aperture definition with macro
- [ ] Block aperture definition
- [x] Draw flash with circle aperture
- [x] Draw flash with rectangle aperture
- [x] Draw flash with obround aperture
- [x] Draw flash with polygon aperture
- [ ] Draw flash with macro aperture
- [ ] Draw flash with block aperture
- [x] Draw line
- [x] Draw clockwise arc
- [x] Draw counterclockwise arc
- [ ] Global mirroring
- [ ] Global rotation
- [ ] Global scaling
- [ ] Create region

Supported **DEPRECATED** Gerber features:

- [ ] Image polarity
- [ ] Image rotation
- [ ] Image mirroring

**IMPORTANT** This feature list is incomplete, it will get longer over time ...

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
