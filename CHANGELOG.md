# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and
this project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

## Pre-Release 3.0.0a4

- Relaxed `pyparsing` dependency requirements to allow for use of `3.2` and above for
  supported Python versions.
- Relaxed `numpy` dependency requirements to allow for use of `2.x` and above for
  supported Python versions.
- Relaxed `pydantic` dependency requirements to allow for use of `2.x` and above for
  supported Python versions.
- Relaxed `pillow` dependency requirements to allow for use of `8.x` and above for
  supported Python versions.
- Relaxed `click` dependency requirements to allow for use of `8.x` and above for
  supported Python versions.
- Relaxed Python version requirement to allow for use of `3.8` and above.
- Removed `pygerber.sequence_tools` module.
- Removed `pygerber.frozen_general_model` module.
- Removed `pygerber.gerber.linter.diagnostic` module.
- Removed `pygerber.warnings` module.
- Updated documentation links to point to stable release documentation.
- Renamed `GerberX3Builder.add_trace()` to `GerberX3Builder.add_line_trace()` to be
  consistent with `GerberX3Builder.add_clockwise_arc_trace()` and
  `GerberX3Builder.add_counter_clockwise_arc_trace()`.
- Added support for Altium implied leading zeros omitted. Contributed by @sjgallagher2
  in #340.
- Added arc drawing in `GerberX3Builder`.
- Added region statement generation to `GerberX3Builder`.
- Added Gerber to PNG, JPEG, TIFF, BMP, WEBP and SVG conversion commands to CLI.
- Added Gerber format command to CLI.
- Extended documentation.

## Pre-Release 3.0.0a3

- Removed legacy error types from `pygerber.gerber.api._errors`.
- Removed `pygerber.common.general_model` module.
- Removed `pygerber.common.immutable_map_model` module.
- Removed `pygerber.common.rgba` module.
- Rename `Project` class from `pygerber.gerber.api` to `CompositeView`.
- Changed `source_code` and `file_type` attributes of `GerberFile` to be read-only.
- Changed return type of `CompositeView.render_with_pillow` to `CompositePillowImage`.
  Interface of `CompositePillowImage` is the same as previously `CompositeView`.
- Changed miniatures displayed by language server to be fixed size due to repeating
  problems with apertures being too small or too large.
- Added custom `__str__` to `CompositeView` and `GerberFile` classes.
- Added `GerberJobFile` class for handling `.gbrjob` files.
- Added `Project` class for grouping multiple `CompositeView` objects.
- Added documentation for `GerberJobFile` and `Project` classes.
- Added `pygerber.vm.shapely` package containing implementation of Gerber vm (renderer)
  using shapely library.
- Added `render_with_shapely` to `GerberFile` class.
- Updated `Quick start` guide.
- Updated many of docstrings in `pygerber.gerber.api` package.
- Restored `pygerber_language_server` command.

## Pre-Release 3.0.0a2

- Removed `Parser2` and related infrastructure. It was already replaced by `Parser` in
  previous release, but I didn't have time to make sure all of dependencies were gone.
- Removed most of the old documentation.
- Moved `pygerber.gerberx3` to `pygerber.gerber`. I acknowledge this is a breaking
  change, but using `gerberx3` as a package name when it in fact contained code mostly
  compatible with more than just X3 was misleading.
- Moved `pygerber.gerber.ast.builder` to `pygerber.builder.gerber`.
- Moved `pygerber.vm.builder` to `pygerber.builder.rvmc`.
- Added new documentation layout.
- Added documentation for `GerberX3Builder` from `pygerber.builder.gerber` module.
- Added `Quick start` guide to documentation.
- Added `pygerber.gerber.pygments`, a Pygments lexer for Gerber files. To use it you
  have to install `pygments` extras package (or just have pygments installed from other
  source).
- Added support for deprecated syntax construct of `D01` with code omitted.
- Changed `pygerber.gerber.formatter` API and structure. Formatter options are no longer
  directly passed to `Formatter` class, they are stored in dedicated `Options` class.
- Added 2 high level formatter API functions available in `pygerber.gerber.formatter`:
  `format`, `formats`.
- Improved docstrings in `pygerber.builder.gerber`
- Improved `pygerber.gerber.formatter` docstrings, especially ones related to formatter
  options.
- Changed `pygerber.gerber.api` to use `pygerber.builder.gerber`. This is a major change
  in how this API works. I am planning to create some guide on how to migrate code from
  PyGerber 2.4.x to 3.x.x, there is placeholder docs page for that.
- Deleted implementation of command line interface. Unfortunately, command line
  interface is not functional right now.

## Pre-Release 3.0.0a1

- Fixed README headers.

## Pre-Release 3.0.0a0

- Added `pygerber.gerberx3.formatter` for formatting Gerber files.
- Added `GerberX3Builder` class for building Gerber code from scratch.
- Redesigned PyGerber Parser implementation and AST classes.
- Added intermediate step between parsing and rendering done by
  `pygerber.gerberx3.compiler`.
- Redesigned rendering principles, now implemented in `pygerber.vm`, supports only
  rendering raster images with Pillow. SVG rendering is planned to be included in 3.0.0
  release.
- Ported language server to new parser.

## Release 2.4.2

- Relaxed `pyparsing` dependency requirements to allow for use of `3.2` and above for
  supported Python versions.
- Relaxed `numpy` dependency requirements to allow for use of `2.x` and above for
  supported Python versions.
- Relaxed `pydantic` dependency requirements to allow for use of `2.x` and above for
  supported Python versions.
- Relaxed `pillow` dependency requirements to allow for use of `8.x` and above for
  supported Python versions.
- Relaxed `click` dependency requirements to allow for use of `8.x` and above for
  supported Python versions.
- Relaxed Python version requirement to allow for use of `3.8` and above.
- Changed documentation deployment flow to include `latest`, `stable` and `dev` links.

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
