# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from PyR3.shortcut.io import export_to

from pygerber.mathclasses import format_bytes
from pygerber.parser.blender.api import render_from_json
from pygerber.parser.blender.api import render_from_toml
from pygerber.parser.blender.api import render_from_yaml


def handle_blender_cli(args):
    print(f"Rendering {args.specfile['filepath']} as {args.specfile['type'].upper()}")
    if args.specfile["type"] == "json":
        render_from_json(args.specfile["filepath"])
    elif args.specfile["type"] == "yaml":
        render_from_yaml(args.specfile["filepath"])
    elif args.specfile["type"] == "toml":
        render_from_toml(args.specfile["filepath"])
    else:
        raise NotImplementedError(
            f"Rendering based on {args.specfile['type']} file format is not supported."
        )
    print(f"Saving to {args.save}")
    export_to(args.save)
    filesize = os.stat(args.save).st_size
    pretty_filesize = format_bytes(filesize)
    print(f"Successfully saved 3D mesh {pretty_filesize}.")
