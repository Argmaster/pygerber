# -*- coding: utf-8 -*-
from __future__ import annotations

from argparse import ArgumentParser, _ArgumentGroup, _MutuallyExclusiveGroup
from pathlib import Path

from PIL._version import __version__ as pillow_version

from .parser.pillow.cli import handle_pillow_cli


def get_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        "pygerber", description="Script for 2D and 3D rendering of Gerber files."
    )
    parser.add_argument(
        "--save",
        "-s",
        type=lambda value: Path(value).absolute(),
        required=True,
        metavar="<savepath>",
        help=(
            "Save path for output render, file format will be automatically. See "
            "https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html "
            "for supported image types for 2D rendering. "
            f"Note that we are currently using pillow {pillow_version}. "
        ),
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=600,
        help="DPI of output image. Affects only 2D renders in --file mode.",
    )
    parser.add_argument(
        "--colors",
        default="copper",
        help="Colors of rendered Gerber image. Affects renders in --file mode.",
    )
    renderer_group: _MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(
        required=True
    )
    renderer_group.add_argument(
        "--pillow",
        "-p",
        help="Select pillow 2D rendering mode.",
        action="store_const",
        const="pillow",
        dest="renderer",
    )
    renderer_group.add_argument(
        "--blender",
        "-b",
        help="Select blender 3D rendering mode.",
        action="store_const",
        const="blender",
        dest="renderer",
    )
    source_group: _MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(
        required=True
    )
    __add_specfile_types_group(source_group)
    return parser


def __add_specfile_types_group(source_group: _ArgumentGroup):
    specfile_types_group: _MutuallyExclusiveGroup = (
        source_group.add_mutually_exclusive_group()
    )

    def validate(spectype_name):
        return lambda value: {
            "type": spectype_name,
            "filepath": Path(value).absolute(),
        }

    for name in ["yaml", "json", "toml"]:
        specfile_types_group.add_argument(
            f"--{name}",
            dest="specfile",
            type=validate(name),
            metavar="<filepath>",
            help=f"Use {name.upper()} specfile, from file <filepath>.",
        )
    specfile_types_group.add_argument(
        "--file",
        dest="specfile",
        type=validate("file"),
        metavar="<filepath>",
        help="Render single gerber file.",
    )


def handle_pygerber_cli(args):
    parser = get_argument_parser()
    args = parser.parse_args(args)
    if args.renderer == "pillow":
        handle_pillow_cli(args)
    elif args.renderer == "blender":
        raise NotImplementedError("Blender rendering is not yet implemented.")
