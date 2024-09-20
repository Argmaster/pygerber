from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class ClockwiseArcAssets(Namespace):
    full = GerberX3Asset(THIS_DIRECTORY / "cw_full.grb")

    half_bot = GerberX3Asset(THIS_DIRECTORY / "half" / "cw_bot_half.grb")
    half_top = GerberX3Asset(THIS_DIRECTORY / "half" / "cw_top_half.grb")
    half_left = GerberX3Asset(THIS_DIRECTORY / "half" / "cw_left_half.grb")
    half_right = GerberX3Asset(THIS_DIRECTORY / "half" / "cw_right_half.grb")

    quarter_bot_left = GerberX3Asset(THIS_DIRECTORY / "quarter" / "cw_bot_left_q.grb")
    quarter_bot_right = GerberX3Asset(THIS_DIRECTORY / "quarter" / "cw_bot_right_q.grb")
    quarter_top_left = GerberX3Asset(THIS_DIRECTORY / "quarter" / "cw_top_left_q.grb")
    quarter_top_right = GerberX3Asset(THIS_DIRECTORY / "quarter" / "cw_top_right_q.grb")

    three_fourth_bot_left = GerberX3Asset(
        THIS_DIRECTORY / "three_fourth" / "cw_bot_left_tf.grb"
    )
    three_fourth_bot_right = GerberX3Asset(
        THIS_DIRECTORY / "three_fourth" / "cw_bot_right_tf.grb"
    )
    three_fourth_top_left = GerberX3Asset(
        THIS_DIRECTORY / "three_fourth" / "cw_top_left_tf.grb"
    )
    three_fourth_top_right = GerberX3Asset(
        THIS_DIRECTORY / "three_fourth" / "cw_top_right_tf.grb"
    )
