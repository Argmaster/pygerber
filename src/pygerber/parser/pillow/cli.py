# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from pygerber.API2D import render_from_json
from pygerber.API2D import render_from_toml
from pygerber.API2D import render_from_yaml
from pygerber.mathclasses import format_bytes
from pygerber.parser.pillow.api import _skip_next_render


def handle_pillow_cli(args):
    if args.dry is True:
        _skip_next_render()
    print(f"Rendering {args.specfile['filepath']} as {args.specfile['type'].upper()}")
    if args.specfile["type"] == "json":
        image = render_from_json(args.specfile["filepath"])
    elif args.specfile["type"] == "yaml":
        image = render_from_yaml(args.specfile["filepath"])
    elif args.specfile["type"] == "toml":
        image = render_from_toml(args.specfile["filepath"])
    else:
        raise NotImplementedError(
            f"Rendering based on {args.specfile['type']} file format is not supported."
        )
    if args.dry is False:
        print(f"Saving to {args.save}")
        image.save(args.save)
        filesize = os.stat(args.save).st_size
        pretty_filesize = format_bytes(filesize)
        print(
            f"Successfully saved image {image.width}x{image.height}, {pretty_filesize}."
        )
    else:
        print("Skipping, dry run.")
