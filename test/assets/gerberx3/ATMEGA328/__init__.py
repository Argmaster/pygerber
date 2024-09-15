from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import ExcellonAsset, GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class ATMEGA328Assets(Namespace):
    bottom_copper = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-B.Cu.gbl")
    bottom_mask = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-B.Mask.gbs")
    bottom_paste = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-B.Paste.gbp")
    bottom_silk = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-B.SilkS.gbo")
    drill = ExcellonAsset(THIS_DIRECTORY / "ATMEGA328_Motor_Board.drl")
    edge_cuts = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-Edge.Cuts.gm1")
    top_copper = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-F.Cu.gtl")
    top_mask = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-F.Mask.gts")
    top_paste = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-F.Paste.gtp")
    top_silk = GerberX3Asset(THIS_DIRECTORY / "ATMEGA328_Motor_Board-F.SilkS.gto")
