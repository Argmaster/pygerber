"""Command line commands of PyGerber."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, TextIO

import click

import pygerber
from pygerber.console.raster_2d_style import (
    STYLE_TO_COLOR_SCHEME,
    get_color_scheme_from_style,
)
from pygerber.gerberx3.api import Rasterized2DLayer, Rasterized2DLayerParams


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
