# PyGerber internal API V2

## Introduction

Since PyGerber 2.2.0, there is alternative improved internal API to PyGerber. It was
created to aid problems with design of API V2 build around `Tokenizer`, `Parser` and
`AbstractBackend` classes and way they interact. They were designed to closely interact
and made extension of PyGerber complicated due to multiple design flaws. Therefore,
implementation of new features was becoming much harder than anticipated. To avoid
breaking backward compatibility and forcing major refactoring, we have decided to
introduce alternative API alongside existing one. To make it easier to distinguish parts
of API V2 modules which contain parts of it contain a suffix or infix `2`, for example
`parser2`, `renderer2`, `commands2`.

API V2 contains new parser implementation, in form of `Parser2` class and new rendering
implementation(s) based on `Renderer2`, eg. `SvgRenderer2` (experimental). We still rely
on original `Tokenizer` and `Token` classes, although their interfaces were extended to
provide integration with `Parser2` separate from how `Parser` (API V1) worked.

New parser from the very begging was equipped with Visitor pattern based design and
allows for easy substitution of implementation of various tokens. Most of Gerber file
state is stored in immutable state which allows for quick jumping back in time.
Additionally state is divided into multiple sub-objects each representing related set of
state properties (compliant to Gerber standard). This separation simplifies process of
sharing information about states with interested parties, eg. draw commands.

## Limited Renderer Coupling

`Parser2` does not rely directly on `Renderer2`, differently than how `Parser`
interacted with `AbstractBackend`. API V2 parser generates command buffer containing
draw commands which describe what should appear in the image. Those commands are later
interpreted by `Renderer2`, but latter one knows nothing about the source of commands,
making it possible to generate in arbitrary ways. Each command makes use of some
aperture in a way described by
[The Gerber Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf).
Set of commands is defined and quite small, same goes for apertures, so implementation
of rendering of them can be very compact.

In API V2 some parts of Gerber images are resolved at parser level into individual
draws. This happens for SR blocks and AB apertures. These concepts doesn't exist at
`Renderer2` level, they are resolved by `Parser2` into correctly transformed series of
draw commands. Macros however remain as apertures and are used to create flashes
consisting of multiple simple commands.

## SVG Rendering

Since release 2.2.0 PyGerber supports converting Gerber files into SVG images with
`SvgRenderer2` class.

To render SVG image from Parser2 output command buffer you need to instantiate
`SvgRenderer2` and feed command buffer object into its `render()` method. In general
`SvgRenderer2` is expected to be one time use only, so using it twice may result in
malformed image.

Here's some sample code showing how to manually create objects from API V2 to parse and
render Gerber file as SVG image.

```python
{{ include_file("test/examples/renderer_2_svg_render.py") }}
```

## Raster Rendering

Since release 2.3.0 PyGerber also supports raster (PNG/JPEG) rendering of images
`RasterRenderer2`.

To render raster image from Parser2 output command buffer you need to instantiate
`RasterRenderer2` and feed command buffer object into its `render()` method. In general
`RasterRenderer2` is expected to be one time use only, so using it twice may result in
malformed image.

```python
{{ include_file("test/examples/renderer_2_raster_render.py") }}
```

`dpmm` option specifies _dots per millimeter_ value used to calculate how many pixels
should single millimeter should contain.
