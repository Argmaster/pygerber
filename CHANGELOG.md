# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and
this project adheres to [Calendar Versioning](https://calver.org/).

## Release 2.1.0

## Release 2.0.1

- Fixed names of Gerber specification files (`.pdf.pdf` extension replaced with `.pdf`)

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
