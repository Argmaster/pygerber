"""Command line commands of PyGerber."""

from __future__ import annotations

import click

import pygerber
from pygerber.gerber.api import FileTypeEnum


@click.group("pygerber")
@click.version_option(version=pygerber.__version__)
def main() -> None:
    """Command line interface of PyGerber, python implementation of Gerber X3/X2
    standard with 2D rendering engine.
    """


@main.command("is-language-server-available")
def _is_language_server_available() -> None:
    from pygerber.gerber.language_server.status import is_language_server_available

    if is_language_server_available():
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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError
