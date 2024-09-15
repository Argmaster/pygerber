from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class KiCadGerberX2Assets(Namespace):
    bottom_copper = GerberX3Asset(THIS_DIRECTORY / "simple_2layer-B_Cu.gbr")
    bottom_mask = GerberX3Asset(THIS_DIRECTORY / "simple_2layer-B_Mask.gbr")
    edge_cuts = GerberX3Asset(THIS_DIRECTORY / "simple_2layer-Edge_Cuts.gbr")
    top_copper = GerberX3Asset(THIS_DIRECTORY / "simple_2layer-F_Cu.gbr")
    top_mask = GerberX3Asset(THIS_DIRECTORY / "simple_2layer-F_Mask.gbr")
    top_paste = GerberX3Asset(THIS_DIRECTORY / "simple_2layer-F_Paste.gbr")
    top_silk = GerberX3Asset(THIS_DIRECTORY / "simple_2layer-F_Silkscreen.gbr")
