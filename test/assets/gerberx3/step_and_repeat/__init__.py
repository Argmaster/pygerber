from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class StepAndRepeatAssets(Namespace):
    cr_x_3 = GerberX3Asset(THIS_DIRECTORY / "00_cr_x_3.grb")
    cr_x_6 = GerberX3Asset(THIS_DIRECTORY / "00_cr_x_6.grb")

    cr_y_3 = GerberX3Asset(THIS_DIRECTORY / "01_cr_y_3.grb")
    cr_y_6 = GerberX3Asset(THIS_DIRECTORY / "01_cr_y_6.grb")

    cr_xy_3_6 = GerberX3Asset(THIS_DIRECTORY / "02_cr_xy_3_6.grb")
    cr_xy_6_6 = GerberX3Asset(THIS_DIRECTORY / "02_cr_xy_6_6.grb")

    cr_x_3_rot_30 = GerberX3Asset(THIS_DIRECTORY / "rot_30" / "00_cr_x_3.grb")
    cr_x_6_rot_30 = GerberX3Asset(THIS_DIRECTORY / "rot_30" / "00_cr_x_6.grb")

    cr_y_3_rot_30 = GerberX3Asset(THIS_DIRECTORY / "rot_30" / "01_cr_y_3.grb")
    cr_y_6_rot_30 = GerberX3Asset(THIS_DIRECTORY / "rot_30" / "01_cr_y_6.grb")

    cr_xy_3_6_rot_30 = GerberX3Asset(THIS_DIRECTORY / "rot_30" / "02_cr_xy_3_6.grb")
    cr_xy_6_6_rot_30 = GerberX3Asset(THIS_DIRECTORY / "rot_30" / "02_cr_xy_6_6.grb")

    cr_xy_2_2_line = GerberX3Asset(THIS_DIRECTORY / "line" / "01_cr_xy_2_2.grb")
    cr_xy_2_2_line_rot_30 = GerberX3Asset(
        THIS_DIRECTORY / "line" / "02_cr_xy_2_2_rot_30.grb"
    )

    cr_xy_2_2_ab = GerberX3Asset(THIS_DIRECTORY / "ab" / "01_cr_xy_2_2.grb")
    cr_xy_2_2_ab_rot_30 = GerberX3Asset(
        THIS_DIRECTORY / "ab" / "02_cr_xy_2_2_rot_30.grb"
    )
