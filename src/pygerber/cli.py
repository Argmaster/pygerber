# -*- coding: utf-8 -*-
from __future__ import annotations

from argparse import ArgumentParser
from argparse import _ArgumentGroup
from argparse import _MutuallyExclusiveGroup
from pathlib import Path

from .parser.pillow.cli import handle_pillow_cli

try:
    from .parser.blender.cli import handle_blender_cli
except ImportError:

    def handle_blender_cli(*_):
        print(
            "bpy module has to be installed to allow 3D rendering, check Installation section of PyGerber's docs."
        )
        exit(-1)


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
            "Save path for output render, file format will be automatically determined from file "
            "extension. Check our documentation for list of supported extensions. https://pygerber.readthedocs.io/en/latest/"
        ),
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
    parser.add_argument(
        "--dry",
        help="Run, but don't render anything.",
        action="store_true",
        default=False,
    )
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


def handle_pygerber_cli(args):
    parser = get_argument_parser()
    args = parser.parse_args(args)
    if args.renderer == "pillow":
        handle_pillow_cli(args)
    elif args.renderer == "blender":
        handle_blender_cli(args)
