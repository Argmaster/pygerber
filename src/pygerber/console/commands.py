"""Command line commands of PyGerber."""

from __future__ import annotations

from pathlib import Path
from typing import Generator, Optional, TextIO

import click

import pygerber
from pygerber.console.raster_2d_style import (
    STYLE_TO_COLOR_SCHEME,
    get_color_scheme_from_style,
)
from pygerber.gerberx3.api import Rasterized2DLayer, Rasterized2DLayerParams
from pygerber.gerberx3.api.v2 import (
    DEFAULT_ALPHA_COLOR_MAP,
    DEFAULT_COLOR_MAP,
    FileTypeEnum,
    GerberFile,
    ImageFormatEnum,
    PixelFormatEnum,
    Project,
)


@click.group("pygerber")
@click.version_option(version=pygerber.__version__)
def main() -> None:
    """Command line interface of PyGerber, python implementation of Gerber X3/X2
    standard with 2D rendering engine.
    """


@main.command("raster-2d")
@click.argument("source", type=click.File())
@click.option(
    "-s",
    "--style",
    default="copper",
    type=click.Choice(list(STYLE_TO_COLOR_SCHEME.keys()), case_sensitive=False),
    help="Color style of the rendered image. When style is 'custom' then option "
    "`--custom` must also be provided. Default is 'copper'.",
)
@click.option(
    "-o",
    "--output",
    type=Path,
    default="output.png",
    help="Path to output file. File format will be inferred from extension, unless "
    "`--format` is given. Default is 'output.png'",
)
@click.option(
    "-f",
    "--format",
    "format_",
    type=str,
    default=None,
    help="Output image format. Can be omitted, then format will be inferred from file"
    "extension or be one of formats supported by Pillow.",
)
@click.option(
    "-c",
    "--custom",
    type=str,
    default=None,
    help="String representing custom set of colors for rendering.\n"
    "Custom color should be a single string consisting of 5 or 7 valid hexadecimal "
    "colors separated with commas. Any color which can be parsed by RGBA type is "
    "accepted.\n"
    "Colors are assigned in order:"
    "\n\n"
    "- background_color\n\n"
    "- clear_color\n\n"
    "- solid_color\n\n"
    "- clear_region_color\n\n"
    "- solid_region_color\n\n"
    "- debug_1_color (optional, by default #ABABAB)\n\n"
    "- debug_2_color (optional, by default #7D7D7D)\n\n"
    "\n\n"
    'eg. `"000000,000000,FFFFFF,000000,FFFFFF"`',
)
@click.option(
    "-d",
    "--dpi",
    type=int,
    default=1000,
    help="DPI of output image, by default 1000.",
)
def raster_2d(
    source: TextIO,
    style: str,
    output: Path,
    format_: Optional[str],
    custom: Optional[str],
    dpi: int,
) -> None:
    """Render rasterized 2D image from Gerber X3/X2 SOURCE file.

    SOURCE - A path to the Gerber file to render.

    List of file formats supported by Pillow:
    https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

    \x08
    RGBA type documentation:
    https://argmaster.github.io/pygerber/latest/reference/pygerber/gerberx3/api/__init__.html#pygerber.common.rgba.RGBA.from_hex
    """  # noqa: D301
    gerber_code = source.read()
    Rasterized2DLayer(
        options=Rasterized2DLayerParams(
            source_code=gerber_code,
            colors=get_color_scheme_from_style(style, custom),
            dpi=dpi,
        ),
    ).render().save(output, format=format_)


@main.command("is-language-server-available")
def _is_language_server_available() -> None:
    from pygerber.gerberx3.language_server import IS_LANGUAGE_SERVER_FEATURE_AVAILABLE

    if IS_LANGUAGE_SERVER_FEATURE_AVAILABLE:
        click.echo("Language server is available.")
    else:
        click.echo("Language server is not available.")


@main.group("render")
def _render() -> None:
    """Render Gerber file with API V2."""


@_render.command("raster")
@click.argument(
    "source",
    type=click.Path(file_okay=True, dir_okay=False, exists=True, readable=True),
)
@click.option(
    "-t",
    "--file-type",
    "file_type",
    type=click.Choice(list(FileTypeEnum.__members__.keys()), case_sensitive=False),
    default=FileTypeEnum.INFER.name,
    help="Type of the Gerber file. Affects what colors are used for rendering. If not "
    "specified, file type will be inferred from extension or .FileFunction attribute.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False),
    default="output.png",
    help="Path to output file.",
)
@click.option(
    "-i",
    "--image-format",
    type=click.Choice(["JPEG", "PNG", "AUTO"], case_sensitive=False),
    default="AUTO",
)
@click.option(
    "-p",
    "--pixel-format",
    type=click.Choice(["RGBA", "RGB"], case_sensitive=False),
    default="RGB",
)
@click.option("-d", "--dpmm", type=int, default=20, help="Dots per millimeter.")
@click.option(
    "-q",
    "--quality",
    type=int,
    default=95,
    help="Compression algorithm quality control parameter.",
)
def _raster(
    source: str,
    file_type: str,
    output: str,
    pixel_format: str,
    image_format: str,
    dpmm: int,
    quality: int,
) -> None:
    """Render Gerber file with API V2 as raster (PNG/JPEG) image."""
    parsed_file = GerberFile.from_file(
        source, file_type=FileTypeEnum(file_type)
    ).parse()

    color_map = DEFAULT_COLOR_MAP

    if pixel_format.upper() == "RGBA":
        color_map = DEFAULT_ALPHA_COLOR_MAP

    color_scheme = color_map[parsed_file.get_file_type()]

    parsed_file.render_raster(
        output,
        color_scheme=color_scheme,
        dpmm=dpmm,
        pixel_format=PixelFormatEnum(pixel_format.upper()),
        image_format=ImageFormatEnum(image_format.lower()),
        quality=quality,
    )


@_render.command("vector")
@click.argument(
    "source",
    type=click.Path(file_okay=True, dir_okay=False, exists=True, readable=True),
)
@click.option(
    "-t",
    "--file-type",
    "file_type",
    type=click.Choice(list(FileTypeEnum.__members__.keys()), case_sensitive=False),
    default=FileTypeEnum.INFER.name,
    help="Type of the Gerber file. Affects what colors are used for rendering. If not "
    "specified, file type will be inferred from extension or .FileFunction attribute.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False),
    default="output.svg",
    help="Path to output file.",
)
@click.option(
    "-s",
    "--scale",
    type=float,
    default=1.0,
    help="Scaling factor applied to the output image.",
)
def _vector(
    source: str,
    file_type: str,
    output: str,
    scale: float,
) -> None:
    """Render Gerber file with API V2 as vector (SVG) image."""
    parsed_file = GerberFile.from_file(
        source, file_type=FileTypeEnum(file_type)
    ).parse()
    color_scheme = DEFAULT_COLOR_MAP[parsed_file.get_file_type()]
    parsed_file.render_svg(output, color_scheme=color_scheme, scale=scale)


@_render.command("project")
@click.argument("files", nargs=-1)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False),
    default="output.png",
    help="Path to output file.",
)
@click.option("-d", "--dpmm", type=int, default=20, help="Dots per millimeter.")
def _project(files: str, output: str, dpmm: int) -> None:
    """Render multiple Gerber files and merge them layer by layer.

    Layers are merged from first to last, thus last layer will be on top.
    """

    def _() -> Generator[GerberFile, None, None]:
        for file in files:
            file_path, *other = file.split("@")

            file_type = FileTypeEnum.INFER
            if len(other) != 0:
                file_type = FileTypeEnum(other[0].upper())

            yield GerberFile.from_file(file_path, file_type)

    Project(list(_())).parse().render_raster(output, dpmm=dpmm)
