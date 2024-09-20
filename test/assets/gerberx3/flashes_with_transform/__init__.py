from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class FlashesWithTransform(Namespace):
    rectangle_rotation_30 = GerberX3Asset(
        THIS_DIRECTORY / "00_rectangle_rotation_30.grb"
    )
    rectangle_rotation_45 = GerberX3Asset(
        THIS_DIRECTORY / "00_rectangle_rotation_45.grb"
    )
    rectangle_rotation_60 = GerberX3Asset(
        THIS_DIRECTORY / "00_rectangle_rotation_60.grb"
    )
    rectangle_rotation_90 = GerberX3Asset(
        THIS_DIRECTORY / "00_rectangle_rotation_90.grb"
    )
    rectangle_rotation_45_mirror_x = GerberX3Asset(
        THIS_DIRECTORY / "10_rectangle_rotation_45_mirror_x.grb"
    )
    rectangle_rotation_45_mirror_y = GerberX3Asset(
        THIS_DIRECTORY / "11_rectangle_rotation_45_mirror_y.grb"
    )
    rectangle_rotation_45_mirror_xy = GerberX3Asset(
        THIS_DIRECTORY / "12_rectangle_rotation_45_mirror_xy.grb"
    )
    rectangle_rotation_30_mirror_x = GerberX3Asset(
        THIS_DIRECTORY / "14_rectangle_rotation_30_mirror_x.grb"
    )
    rectangle_rotation_30_mirror_y = GerberX3Asset(
        THIS_DIRECTORY / "15_rectangle_rotation_30_mirror_y.grb"
    )
    rectangle_rotation_30_mirror_xy = GerberX3Asset(
        THIS_DIRECTORY / "16_rectangle_rotation_30_mirror_xy.grb"
    )
