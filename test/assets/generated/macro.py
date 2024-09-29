from __future__ import annotations

from pygerber.builder.gerber import GerberX3Builder
from pygerber.gerber.ast.nodes import File


def get_custom_circle_local_2_0() -> File:
    builder = GerberX3Builder()
    d10 = builder.new_pad().circle(0.1)
    builder.add_pad(d10, (0, 0))

    d11 = builder.new_pad().custom().add_circle(1, (2, 0), rotation=0.0).create()
    builder.add_pad(d11, (0, 0))

    return builder.get_code().raw


def get_custom_circle_local_2_0_rot_30() -> File:
    builder = GerberX3Builder()
    d10 = builder.new_pad().circle(0.1)
    builder.add_pad(d10, (0, 0))

    d11 = builder.new_pad().custom().add_circle(1, (2, 0), rotation=30.0).create()
    builder.add_pad(d11, (0, 0))

    return builder.get_code().raw


def get_custom_circle_local_2_0_ring_rot_30() -> File:
    builder = GerberX3Builder()
    d10 = builder.new_pad().circle(0.1)
    builder.add_pad(d10, (0, 0))

    for rot in range(0, 360, 30):
        pad = builder.new_pad().custom().add_circle(1, (2, 0), rotation=rot).create()
        builder.add_pad(pad, (0, 0))

    return builder.get_code().raw
