from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class CounterClockwiseArcAssets(Namespace):
    full = GerberX3Asset(THIS_DIRECTORY / "ccw_full.grb")
    half_bot = GerberX3Asset(THIS_DIRECTORY / "half" / "ccw_bot_half.grb")
    half_top = GerberX3Asset(THIS_DIRECTORY / "half" / "ccw_top_half.grb")
    half_left = GerberX3Asset(THIS_DIRECTORY / "half" / "ccw_left_half.grb")
    half_right = GerberX3Asset(THIS_DIRECTORY / "half" / "ccw_right_half.grb")
    quarter_bot_left = GerberX3Asset(THIS_DIRECTORY / "quarter" / "ccw_bot_left_q.grb")
    quarter_bot_right = GerberX3Asset(
        THIS_DIRECTORY / "quarter" / "ccw_bot_right_q.grb"
    )
    quarter_top_left = GerberX3Asset(THIS_DIRECTORY / "quarter" / "ccw_top_left_q.grb")
    quarter_top_right = GerberX3Asset(
        THIS_DIRECTORY / "quarter" / "ccw_top_right_q.grb"
    )
    three_fourth_bot_left = GerberX3Asset(
        THIS_DIRECTORY / "three_fourth" / "ccw_bot_left_tf.grb"
    )
    three_fourth_bot_right = GerberX3Asset(
        THIS_DIRECTORY / "three_fourth" / "ccw_bot_right_tf.grb"
    )
    three_fourth_top_left = GerberX3Asset(
        THIS_DIRECTORY / "three_fourth" / "ccw_top_left_tf.grb"
    )
    three_fourth_top_right = GerberX3Asset(
        THIS_DIRECTORY / "three_fourth" / "ccw_top_right_tf.grb"
    )
