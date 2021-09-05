# -*- coding: utf-8 -*-
from __future__ import annotations
from math import inf
from functools import lru_cache

import os
from typing import Dict, List, Tuple

from pygerber.parser.pillow.api import (
    render_from_json,
    render_from_toml,
    render_from_yaml,
)

UNIT_MAP_TYPE = Dict[Tuple[float, float], str]

_ByteUnits = {
        (0, 1024): "B",
        (1024, 1024 ** 2): "KiB",
        (1024 ** 2, 1024 ** 3): "MiB",
        (1024 ** 3, 1024 ** 4): "GiB",
        (1024 ** 4, inf): "TiB",
    }

def format_bytes(
    val: float,
) -> str:
    abs_val = abs(val)
    for range, unit in _ByteUnits.items():
        if range[0] <= abs_val < range[1]:
            return f"{val/range[0]:.1f} {unit}"


def handle_pillow_cli(args):
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
    print(f"Saving to {args.save}")
    image.save(args.save)
    filesize = os.stat(args.save).st_size
    pretty_filesize = format_bytes(filesize)
    print(f"Successfully saved image {image.width}x{image.height}, {pretty_filesize}.")
