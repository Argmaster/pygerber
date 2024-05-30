# Command line usage

In addition to API, PyGerber also offers simple command line interface (CLI) for
rendering Gerber files to raster and vector image formats. Although CLI is not as
powerful as API, it is still useful for quick rendering.

## Single file rendering

Single Gerber file can be rendered to both vector (SVG) and raster (PNG/JPEG) image
formats.

Here is a minimalistic example of rendering a single Gerber file to PNG image:

```
pygerber render raster src/pygerber/examples/simple_2layer-F_Cu.gbr -o main.png
```

PyGerber allows rendering rendering to PNG and JPEG formats. Additionally quality and
size of the image can be controlled using `-q/--quality` and `-d/--dpmm` flags. For full
list of available flags use `--help` flag.

```
pygerber render raster --help
```

For comparison, here is an example of rendering the same Gerber file to SVG image:

```
pygerber render vector src/pygerber/examples/simple_2layer-F_Cu.gbr -o main.svg
```

## Multi-file project rendering

PyGerber also supports rendering multi-file projects. This is useful when you have
multiple Gerber files that represent different layers of the same PCB and you want to
generate a single image stacking them on top of each other with single command.

This can be done by providing list of paths to gerber files to `pygerber render project`
command.

Each path can be suffixed with `@` and layer type name. This will affect color palette
used for rendering individual layers. For full list of available layer types check out
`FileTypeEnum` values. Layer names are case-insensitive.

```bash
pygerber render project src/pygerber/examples/simple_2layer-F_Cu.gbr@copper src/pygerber/examples/simple_2layer-F_Mask.gbr@mask src/pygerber/examples/simple_2layer-F_Paste.gbr@paste src/pygerber/examples/simple_2layer-F_Silkscreen.gbr@silk
```

When layer type is not provided, file type will be inferred from extension or file
attributes. If neither of those methods succeeds, `FileTypeEnum.UNDEFINED` will be used
resulting in use of debug color palette.

Thanks to file type inference, command below should produce the same result as the one
above:

```bash
pygerber render project src/pygerber/examples/simple_2layer-F_Cu.gbr src/pygerber/examples/simple_2layer-F_Mask.gbr src/pygerber/examples/simple_2layer-F_Paste.gbr src/pygerber/examples/simple_2layer-F_Silkscreen.gbr
```
