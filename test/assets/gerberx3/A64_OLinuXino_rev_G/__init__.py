from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import ExcellonAsset, GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class A64_OlinuXino_Rev_G(Namespace):  # noqa: N801
    A64_OlinuXino_Rev_G_B_Cu = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-B_Cu.gbr"
    )
    A64_OlinuXino_Rev_G_B_Mask = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-B_Mask.gbr"
    )
    A64_OlinuXino_Rev_G_B_Paste = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-B_Paste.gbr"
    )
    A64_OlinuXino_Rev_G_B_SilkS = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-B_SilkS.gbr"
    )
    A64_OlinuXino_Rev_G_Edge_Cuts = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-Edge_Cuts.gbr"
    )
    A64_OlinuXino_Rev_G_F_Cu = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-F_Cu.gbr"
    )
    A64_OlinuXino_Rev_G_F_Mask = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-F_Mask.gbr"
    )
    A64_OlinuXino_Rev_G_F_Paste = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-F_Paste.gbr"
    )
    A64_OlinuXino_Rev_G_F_SilkS = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-F_SilkS.gbr"
    )
    A64_OlinuXino_Rev_G_In1_Cu = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-In1_Cu.gbr"
    )
    A64_OlinuXino_Rev_G_In2_Cu = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-In2_Cu.gbr"
    )
    A64_OlinuXino_Rev_G_In3_Cu = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-In3_Cu.gbr"
    )
    A64_OlinuXino_Rev_G_In4_Cu = GerberX3Asset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-In4_Cu.gbr"
    )
    A64_OlinuXino_Rev_G_NPTH = ExcellonAsset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-NPTH.drl"
    )
    A64_OlinuXino_Rev_G_PTH = ExcellonAsset(
        THIS_DIRECTORY / "A64-OlinuXino_Rev_G-PTH.drl"
    )
