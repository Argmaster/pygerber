# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and
this project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

## Release 2.4.1

- Added support for comment based attributes (#217)
- Fixed incorrect rotation of rectangle flashes (#243)
- Removed PyYAML dependency (#221)
- Added tests for language server (#227)
- Added tests for console interface (#223)

## Release 2.4.0

- Added command line interface utilizing API V2 for rendering Gerber files to images.
  This includes interface for rendering PNG, JPEG and SVG images and multi-file projects
  to single PNG/JPEG image.
- Added support for inferring file type from file extension or `.FileFunction` file
  attribute. This mechanism is used by default by API V2 based command line interface.
- Refactored test suite and dropped testing of code related to `Parser` class originally
  included in `PyGerber` 2.0.0. Currently only `Parser2` related code is actively
  tested.

## Release 2.3.2

- Fixed clockwise arc rendering in raster renderer. Reported by @tgbl-mk (#203). Fixed
  by @Argmaster in #205.
- Fixed empty comment parsing. Reported by @lookme2 (#198). Fixed by @Argmaster in #201.
- Disabled MacOS test suite due to consistent failures during Python installation on
  `macos-latest` GitHub hosted machines.

## Release 2.3.1

- Added support for rotation of code 21 center line macro primitive in SVG and Raster
  renderers. Support is not exhaustive, it will be extended whenever extension is
  requested by users.
- Fixed bug causing macro flashes to be partially cut off in images rendered with SVG
  renderer.
- Fixed incorrect version string in `pygerber.__version__` and reported by
  `pygerber --version`.

## Release 2.3.0

- Added full support for transforms (LP, LM, LR, LS commands) in Parser2.
- Fixed titles in Parser2 and Parser feature support documentation. They were swapped.
- Fixed bug causing SvgRenderer2 to incorrectly render masks in some cases.
- Optimized SvgRenderer2 group and mask usage to reduce file size and memory usage of
  software displaying output SVGs.
- Fixed parsing of attributes without value.
- Updated documentation to mention deprecation of API V1 elements and changed order of
  pages to better expose API V2.
- Added example files shipped with PyGerber for testing and demonstration purposes. They
  can be accessed via `pygerber.examples` module.
- Added new `pygerber.gerberx3.api.v2` module with new high level utilizing API V2
  capabilities. This module is mend to replace API V1 in future releases.
- Added new API for rendering multiple Gerber files at once into single image. Available
  as part of `pygerber.gerberx3.api.v2` module with use of `Project` class.

## Release 2.2.1

- Fixed rendering of first macro flash.
- Added reference page for SvgRenderer2 in docs.
- Fixed duplicated element prefixes in docs.
- Fixed supported feature counts in docs.
- Updated `README.md` feature support links.

## Release 2.2.0

- Added alternative parser implementation, `pygerber.gerberx3.parser2.parser2.Parser2`
  class.
- Added introspection interface based on new Parser2 class.
- Added macro support to Parser2 class which was not previously available in Parser
  class.
- Added API for customizing Token classes used by Tokenizer. `Tokenizer` class now
  accepts optional `options` parameter of class `TokenizerOptions`.
- Added documentation for introspection.
- Added experimental SVG backend for Gerber code with Parser2 generated command buffers.
- Changed documentation layout to improve readability.
- Fixed switching to single quadrant mode being ignored.
- Refactored feature support documentation.

## Release 2.1.1

- Fixed incorrect bounding box prediction for displaced drawings (#105).
- Added 3.12 as supported in package tags.
- Fixed documentation links in `README.md` and `pyproject.toml`.

## Release 2.1.0

- Fixed #37
- Added latest Gerber spec file revision 2023.08 to documentation.
- Added command line interface for PyGerber 2D rendering.
- Added Gerber X3/X2 language server which can be acquired with
  `pip install pygerber[language-server]`. Currently server capabilities include hover
  messages with Gerber reference cited and minimal amount of suggestions. We are
  planning to further extend this server in future releases.
- Added `is-language-server-available` CLI command for checking if
  `pygerber[language-sever]` is available.
- Added support for arc region boundaries (#61).
- Added warning messages whenever zero surface flash is created.
- Improved documentation for many of supported Gerber commands. This documentation is
  used by language server to provide specification reference.
- Refactored tokenizer implementation, as a result #67 was fixed and #64 is no longer an
  issue in some cases.

## Release 2.0.2

- Fixed incorrect bounding box prediction for displaced drawings (#105).
- Added 3.12 as supported in package tags.
- Fixed documentation links in `README.md` and `pyproject.toml`.

## Release 2.0.1

- Fixed names of Gerber specification files (`.pdf.pdf` extension replaced with `.pdf`)
- Added `draw_region_outlines` option (disabled by default) which controls whether lines
  which make up a region boundary should be drawn after region is filled. KiCAD seem to
  assume that those boundaries are not drawn and region outline is 1px instead of
  thickness of aperture.
- Changed `Decimal` precision to 60 decimal places.
- Changed precision of `INCH_TO_MM_MULTIPLIER` (now its 25.4) and
  `MM_TO_INCH_MULTIPLIER` (dynamically calculated with `Decimal`).
- Changed circle aperture to make result better match expectations and `KiCAD`
  reference.
- Fixed warning message logged every time a valid region was created to show up only
  when region is not valid.
- Added warnings for zero surface aperture draws.

## Release 2.0.0

- Added Gerber X3 format tokenizer with support for selective feature support:

  - Supported Gerber X3 features: `G04`, `MO`, `FS`, `AD`, `AM`, `Dnn` (nn≥10), `D01`,
    `D02`, `D03`, `G01`, `G02`, `G03`, `G75`, `LP`, `LM`, `LR`, `LS`, `G36`, `G37`,
    `AB`, `SR`, `TF`, `TA`, `TO`,`TD`, `M02`.

  - Supported **DEPRECATED** Gerber features: `G54`, `G70`, `G71`, `G90`, `G91`, `G74`,
    `M00`, `M01`, `IP`, `LN`,
    `Combining G01/G02/G03 and D01/D02/D03 in a single command`,
    `Coordinate Data without Operation Code`, `Style Variations in Command Codes`, `FS`,
    `Draws and Arcs with Rectangular Apertures`.

  For more detailed descriptions of supported features please refer to documentation or
  README.md.

- Added Gerber X3 format parser with support for selective feature support:

  - Supported Gerber X3 features: `G04`, `MO`, `FS`, `AD`, `AM`, `Dnn` (nn≥10), `D01`,
    `D02`, `D03`, `G01`, `G02`, `G03`, `G75`, `LP`, `LM`, `LR`, `LS`, `G36`, `G37`,
    `M02`.

  - Supported **DEPRECATED** Gerber features: `G54`, `G70`, `G71`, `G90`, `G91`, `G74`,
    `M00`, `M01`, `IP`, `LN`, `Combining G01/G02/G03 and D01 in a single command`,
    `Coordinate Data without Operation Code`, `Style Variations in Command Codes`,
    `Draws and Arcs with Rectangular Apertures`.

  For more detailed descriptions of supported features please refer to documentation or
  README.md.

- Added rendering backend capable of producing 2D rasterized images based on parser
  instructions. Supported drawing elements:
  - Aperture definition with circle
  - Aperture definition with rectangle
  - Aperture definition with obround
  - Aperture definition with polygon
  - Draw flash with circle aperture
  - Draw flash with rectangle aperture
  - Draw flash with obround aperture
  - Draw flash with polygon aperture
  - Draw line
  - Draw clockwise arc
  - Draw counterclockwise arc
