"""Command line commands of PyGerber."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Optional

import click

from pygerber.gerber import formatter
from pygerber.gerber.api import Color, FileTypeEnum, GerberFile, Style
from pygerber.gerber.api._composite_view import CompositeView
from pygerber.vm.shapely.vm import is_shapely_available
from pygerber.vm.types.color import InvalidHexColorLiteralError


@click.group("gerber")
def gerber() -> None:
    """Gerber format related commands."""


@gerber.group("convert")
def convert() -> None:
    """Convert Gerber image to different image format."""


def _get_file_type_option() -> Callable[[click.decorators.FC], click.decorators.FC]:
    return click.option(
        "-t",
        "--file-type",
        "file_type",
        type=click.Choice(list(FileTypeEnum.__members__.keys()), case_sensitive=False),
        default=FileTypeEnum.INFER.name,
        help=(
            "Type (function) of the Gerber file. Affects what colors are used for "
            "rendering. If not  specified, file type will be inferred from extension "
            "or .FileFunction attribute."
        ),
    )


def _get_style_option() -> Callable[[click.decorators.FC], click.decorators.FC]:
    return click.option(
        "-s",
        "--style",
        type=click.Choice(
            [*Style.presets.get_styles(), "CUSTOM"], case_sensitive=False
        ),
        default=None,
        help=(
            "Direct style override. When specified, this will override style implied "
            "by file type. When set to CUSTOM, you have to use -f/--foreground and "
            "-b/--background to specify foreground and background colors."
        ),
    )


def _get_foreground_option() -> Callable[[click.decorators.FC], click.decorators.FC]:
    return click.option(
        "-f",
        "--foreground",
        type=str,
        default=None,
        help=(
            "Foreground color in hex format. Only used when --style is set to CUSTOM. "
            "Example: `#FF0000`, `#` is accepted but not mandatory."
        ),
    )


def _get_background_option() -> Callable[[click.decorators.FC], click.decorators.FC]:
    return click.option(
        "-b",
        "--background",
        type=str,
        default=None,
        help=(
            "Background color in hex format. Only used when --style is set to CUSTOM. "
            "Example: `#FF0000`, `#` is accepted but not mandatory."
        ),
    )


def _get_raster_implementation_option(
    *vals: str,
) -> Callable[[click.decorators.FC], click.decorators.FC]:
    return click.option(
        "-i",
        "--implementation",
        type=click.Choice(vals, case_sensitive=False),
        default=vals[0],
        help="Name of rendering Virtual Machine to be used.",
    )


def _get_output_file_option() -> Callable[[click.decorators.FC], click.decorators.FC]:
    return click.option(
        "-o",
        "--output",
        type=click.Path(dir_okay=False),
        default="output.png",
        help="Path to output file.",
    )


def _get_dpmm_option() -> Callable[[click.decorators.FC], click.decorators.FC]:
    return click.option(
        "-d",
        "--dpmm",
        type=int,
        default=100,
        help="Dots per millimeter.",
    )


def _get_source_file_argument() -> Callable[[click.decorators.FC], click.decorators.FC]:
    return click.argument(
        "source",
        type=click.Path(file_okay=True, dir_okay=False, exists=True, readable=True),
    )


@convert.command("png")
@_get_source_file_argument()
@_get_output_file_option()
@_get_dpmm_option()
@_get_file_type_option()
@_get_style_option()
@_get_foreground_option()
@_get_background_option()
@_get_raster_implementation_option("pillow")
def png(
    source: str,
    output: str,
    file_type: str,
    style: Optional[str],
    foreground: Optional[str],
    background: Optional[str],
    dpmm: int,
    implementation: str,
) -> None:
    """Convert Gerber image file to PNG image."""
    style_obj = _sanitize_style(style, foreground, background)
    file = GerberFile.from_file(source, file_type=FileTypeEnum(file_type.upper()))

    if implementation.lower() == "pillow":
        result = file.render_with_pillow(style_obj, dpmm)
        result.save_png(output)

    else:
        msg = f"Implementation {implementation!r} is not supported."
        raise NotImplementedError(msg)


def _sanitize_style(
    style: Optional[str],
    foreground: Optional[str],
    background: Optional[str],
) -> Optional[Style]:
    style_obj: Optional[Style] = None

    if style is not None:
        style = style.upper()

        if style == "CUSTOM":
            if foreground is None or background is None:
                option_name = "foreground" if foreground is None else "background"
                msg = (
                    "When using CUSTOM style, both foreground and background must be "
                    "specified."
                )
                raise click.BadOptionUsage(option_name, msg)

            try:
                background_color = Color.from_hex(background)
            except InvalidHexColorLiteralError as e:
                msg = f"Invalid hex color literal: {e!r}"
                raise click.BadOptionUsage("background", msg) from e

            try:
                foreground_color = Color.from_hex(foreground)
            except InvalidHexColorLiteralError as e:
                msg = f"Invalid hex color literal: {e!r}"
                raise click.BadOptionUsage("background", msg) from e

            style_obj = Style(
                background=background_color,
                foreground=foreground_color,
            )

        else:
            style_obj = Style.presets.get_styles().get(style)

            if style_obj is None:
                option_name = "style"
                msg = f"Style {style!r} is not recognized."
                raise click.BadOptionUsage(option_name, msg)

    return style_obj


@convert.command("jpeg")
@_get_source_file_argument()
@_get_output_file_option()
@_get_dpmm_option()
@_get_file_type_option()
@_get_style_option()
@_get_foreground_option()
@_get_background_option()
@_get_raster_implementation_option("pillow")
@click.option(
    "-q",
    "--quality",
    type=int,
    default=95,
    help="Compression algorithm quality control parameter.",
)
def jpeg(  # noqa: PLR0913
    source: str,
    output: str,
    file_type: str,
    style: Optional[str],
    foreground: Optional[str],
    background: Optional[str],
    dpmm: int,
    implementation: str,
    quality: int,
) -> None:
    """Convert Gerber image file to JPEG image."""
    style_obj = _sanitize_style(style, foreground, background)
    file = GerberFile.from_file(source, file_type=FileTypeEnum(file_type.upper()))

    if implementation.lower() == "pillow":
        result = file.render_with_pillow(style_obj, dpmm)
        result.save_jpeg(output, quality=quality)

    else:
        msg = f"Implementation {implementation!r} is not supported."
        raise NotImplementedError(msg)


@convert.command("tiff")
@_get_source_file_argument()
@_get_output_file_option()
@_get_dpmm_option()
@_get_file_type_option()
@_get_style_option()
@_get_foreground_option()
@_get_background_option()
@_get_raster_implementation_option("pillow")
@click.option(
    "-c",
    "--compression",
    type=click.Choice(
        [
            "group3",
            "group4",
            "jpeg",
            "lzma",
            "packbits",
            "tiff_adobe_deflate",
            "tiff_ccitt",
            "tiff_lzw",
            "tiff_raw_16",
            "tiff_sgilog",
            "tiff_sgilog24",
            "tiff_thunderscan",
            "webp",
            "zstd",
        ]
    ),
    default="lzma",
    help="Compression algorithm.",
)
@click.option(
    "-q",
    "--quality",
    type=int,
    default=95,
    help=(
        "Compression algorithm quality control parameter, applicable "
        "only for JPEG compression."
    ),
)
def tiff(  # noqa: PLR0913
    source: str,
    output: str,
    file_type: str,
    style: Optional[str],
    foreground: Optional[str],
    background: Optional[str],
    dpmm: int,
    implementation: str,
    compression: str,
    quality: int,
) -> None:
    """Convert Gerber image file to TIFF image."""
    style_obj = _sanitize_style(style, foreground, background)
    file = GerberFile.from_file(source, file_type=FileTypeEnum(file_type.upper()))

    if implementation.lower() == "pillow":
        result = file.render_with_pillow(style_obj, dpmm)

        opts: dict[str, Any] = {"compression": compression}
        if compression == "jpeg":
            opts["quality"] = quality

        result.save_tiff(output, **opts)

    else:
        msg = f"Implementation {implementation!r} is not supported."
        raise NotImplementedError(msg)


@convert.command("bmp")
@_get_source_file_argument()
@_get_output_file_option()
@_get_dpmm_option()
@_get_file_type_option()
@_get_style_option()
@_get_foreground_option()
@_get_background_option()
@_get_raster_implementation_option("pillow")
def bmp(
    source: str,
    output: str,
    file_type: str,
    style: Optional[str],
    foreground: Optional[str],
    background: Optional[str],
    dpmm: int,
    implementation: str,
) -> None:
    """Convert Gerber image file to BMP image."""
    style_obj = _sanitize_style(style, foreground, background)
    file = GerberFile.from_file(source, file_type=FileTypeEnum(file_type.upper()))

    if implementation.lower() == "pillow":
        result = file.render_with_pillow(style_obj, dpmm)
        result.save_bmp(output)

    else:
        msg = f"Implementation {implementation!r} is not supported."
        raise NotImplementedError(msg)


@convert.command("webp")
@_get_source_file_argument()
@_get_output_file_option()
@_get_dpmm_option()
@_get_file_type_option()
@_get_style_option()
@_get_foreground_option()
@_get_background_option()
@_get_raster_implementation_option("pillow")
@click.option(
    "-l",
    "--lossless",
    is_flag=True,
    default=False,
    help="Instructs the WebP writer to use lossless compression.",
)
@click.option(
    "-q",
    "--quality",
    type=int,
    default=80,
    help=(
        "Compression algorithm quality control parameter, applicable "
        "only for JPEG compression."
    ),
)
def webp(  # noqa: PLR0913
    source: str,
    output: str,
    file_type: str,
    style: Optional[str],
    foreground: Optional[str],
    background: Optional[str],
    dpmm: int,
    implementation: str,
    lossless: str,
    quality: int,
) -> None:
    """Convert Gerber image file to WEBP image."""
    style_obj = _sanitize_style(style, foreground, background)
    file = GerberFile.from_file(source, file_type=FileTypeEnum(file_type.upper()))

    if implementation.lower() == "pillow":
        result = file.render_with_pillow(style_obj, dpmm)
        result.save_webp(output, lossless=lossless, quality=quality)

    else:
        msg = f"Implementation {implementation!r} is not supported."
        raise NotImplementedError(msg)


if is_shapely_available():

    @convert.command("svg")
    @_get_source_file_argument()
    @_get_output_file_option()
    @_get_file_type_option()
    @_get_style_option()
    @_get_foreground_option()
    @_get_background_option()
    @_get_raster_implementation_option("shapely")
    def svg(
        source: str,
        output: str,
        file_type: str,
        style: Optional[str],
        foreground: Optional[str],
        background: Optional[str],
        implementation: str,
    ) -> None:
        """Convert Gerber image file to SVG image."""
        style_obj = _sanitize_style(style, foreground, background)
        file = GerberFile.from_file(source, file_type=FileTypeEnum(file_type.upper()))

        if implementation.lower() == "shapely":
            result = file.render_with_shapely(style_obj)
            result.save(output)

        else:
            msg = f"Implementation {implementation!r} is not supported."
            raise NotImplementedError(msg)


@gerber.command("format")
@click.argument(
    "source",
    type=click.Path(file_okay=True, dir_okay=False),
)
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=True, dir_okay=False),
    default=Path("output.gbr"),
    help="Path to output file.",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(file_okay=True, dir_okay=False),
    default=None,
    help="Path to configuration file. Please have a look into documentation in command "
    "line section to see available formatter options.",
)
@click.option(
    "-i",
    "--inline-config",
    type=str,
    default=None,
    help="JSON string containing dictionary with configuration options. Please have a "
    "look into documentation in command line section to see available formatter "
    "options.",
)
def format_cmd(
    source: str,
    output: str,
    config: Optional[str],
    inline_config: Optional[str],
) -> None:
    """Format Gerber file.

    SOURCE - path to file which is supposed to be formatted.
    """
    config_type: Literal["json"] = "json"

    if config is not None:
        if inline_config is not None:
            msg = (
                "Both --config and --inline-config options cannot be used at the "
                "same time."
            )
            raise click.BadOptionUsage("inline-config", msg)

        config_path = Path(config)
        if config_path.suffix == ".json":
            inline_config = config_path.read_text("utf-8")
        else:
            msg = "Only JSON configuration files are supported."
            raise click.BadOptionUsage("config", msg)

    options: Optional[formatter.Options] = None

    if inline_config is not None:
        if config_type == "json":
            options = formatter.Options(**json.loads(inline_config))
        else:
            raise NotImplementedError

    output_path = Path(output)
    file = GerberFile.from_file(source)

    with output_path.open("w") as f:
        file.format(f, options=options)


@gerber.group("merge-convert")
def merge_convert() -> None:
    """Convert multiple Gerber images to different image format and merge them into one
    image (stack on top of each other).
    """


@merge_convert.command("png")
@click.argument("sources", nargs=-1)
@_get_output_file_option()
@_get_dpmm_option()
@_get_file_type_option()
@_get_raster_implementation_option("pillow")
def merge_convert_png(
    sources: str,
    output: str,
    file_type: str,
    dpmm: int,
    implementation: str,
) -> None:
    """Convert multiple Gerber images to PNG image and merge them into one image.

    Images are merged from first to last, thus fist layer is bottom most, last layer
    is topmost, unobstructed.

    SOURCES - paths to files which are supposed to be rendered and merged.
    """
    view = CompositeView(
        GerberFile.from_file(source, file_type=FileTypeEnum(file_type.upper()))
        for source in sources
    )

    if implementation.lower() == "pillow":
        result = view.render_with_pillow(dpmm)
        result.save_png(output)

    else:
        msg = f"Implementation {implementation!r} is not supported."
        raise NotImplementedError(msg)


@merge_convert.command("jpeg")
@click.argument("sources", nargs=-1)
@_get_output_file_option()
@_get_dpmm_option()
@_get_file_type_option()
@_get_raster_implementation_option("pillow")
def merge_convert_jpeg(
    sources: str,
    output: str,
    file_type: str,
    dpmm: int,
    implementation: str,
) -> None:
    """Convert multiple Gerber images to JPEG image and merge them into one image.

    Images are merged from first to last, thus fist layer is bottom most, last layer
    is topmost, unobstructed.

    SOURCES - paths to files which are supposed to be rendered and merged.
    """
    view = CompositeView(
        GerberFile.from_file(source, file_type=FileTypeEnum(file_type.upper()))
        for source in sources
    )

    if implementation.lower() == "pillow":
        result = view.render_with_pillow(dpmm)
        result.save_jpeg(output)

    else:
        msg = f"Implementation {implementation!r} is not supported."
        raise NotImplementedError(msg)


@gerber.command("lint")
@click.argument("files", nargs=-1)
@click.option(
    "-r",
    "--rules",
    type=str,
    multiple=True,
    help=(
        "Linting rules to be applied. Option can be used multiple times and accepts "
        "comma separated list of rules, eg. `-r DEP001,DEP002,DEP003 -r DEP004`. "
        "If not specified, all available rules will be applied."
    ),
)
def lint(files: str, rules: list[str]) -> None:
    """Lint Gerber files with specified rules."""
    from pygerber.gerber.linter import lint
    from pygerber.gerber.parser import parse

    if len(files) == 0:
        msg = "At least one file must be specified."
        raise click.UsageError(msg)

    def _parse_rules(rules: list[str]) -> Iterable[str]:
        for rule in rules:
            yield from rule.split(",")

    rules = list(_parse_rules(rules))

    for file in files:
        path = Path(file).expanduser().resolve()

        ast = parse(path.read_text())
        violations = lint(ast, rules=rules)

        for violation in violations:
            click.echo(
                f"{path.as_posix()}:{violation.line}:{violation.column} "
                f"{violation.rule_id}: {violation.title}"
            )


@gerber.command("list-lint-rules")
@click.option(
    "-q", "--quiet", is_flag=True, help="Print only rule names without descriptions."
)
def list_lint_rules(*, quiet: bool) -> None:
    """List available linting rules."""
    from pygerber.gerber.linter.rules import RULE_REGISTRY

    for rule_id in RULE_REGISTRY:
        if quiet:
            click.echo(rule_id)
        else:
            rule = RULE_REGISTRY[rule_id]()
            click.echo(f"{rule_id}: {rule.get_violation_title()}")
