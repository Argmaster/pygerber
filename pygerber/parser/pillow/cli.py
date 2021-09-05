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


@lru_cache
def _mk_unit_map(base_unit: str = "{prefix}J/mol", step=1000) -> UNIT_MAP_TYPE:
    """Create unit mapping dictionary

    Args:
        base_unit (str, optional): formatable string. Defaults to "{prefix}J/mol".

    Returns:
        UNIT_MAP_TYPE: map with SI prefixes from p to G
    >>> _mk_unit_map("{prefix}J/mol")
    {(-inf, 1e-09): 'pJ/mol', (1e-09, 1e-06): 'nJ/mol', (1e-06, 0.001): 'µJ/mol', (0.001, 1): 'mJ/mol', (1, 1000.0): 'J/mol', (1000.0, 1000000.0): 'kJ/mol', (1000000.0, 1000000000.0): 'MJ/mol', (1000000000.0, 1000000000000.0): 'GJ/mol', (1000000000000.0, inf): 'GJ/mol'}
    """
    return {
        (-inf, step ** -3): base_unit.format(prefix="p"),
        (step ** -3, step ** -2): base_unit.format(prefix="n"),
        (step ** -2, step ** -1): base_unit.format(prefix="µ"),
        (step ** -1, 1): base_unit.format(prefix="m"),
        (step ** 0, step): base_unit.format(prefix=""),
        (step, step ** 2): base_unit.format(prefix="k"),
        (step ** 2, step ** 3): base_unit.format(prefix="M"),
        (step ** 3, step ** 4): base_unit.format(prefix="G"),
        (step ** 4, inf): base_unit.format(prefix="T"),
    }


def pretty_unit(
    val: float,
    __unit_map: UNIT_MAP_TYPE = _mk_unit_map("{prefix}J/mol"),
) -> str:
    """Stringify given value and choose appropriate SI unit
    prefix as so the value is not longer than 6 digits

    Args:
        val (float): value (in J/mol) to stringify

    Returns:
        str: string repr with unit included

    >>> pretty_unit(7425.878378172057)
    '7.426 kJ/mol'
    """
    abs_val = abs(val)
    for range, unit in __unit_map.items():
        if range[0] <= abs_val < range[1]:
            return f"{val/range[0]:.3f} {unit}"


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
    pretty_filesize = pretty_unit(filesize, _mk_unit_map("{prefix}B", step=1024))
    print(
        f"Successfully saved image {image.width}x{image.height}, {pretty_filesize}."
    )
