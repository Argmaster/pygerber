from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class GerberSpecExampleAssets(Namespace):
    asset_2_1 = GerberX3Asset(THIS_DIRECTORY / "2.1" / "source.grb")
    asset_2_11_1 = GerberX3Asset(THIS_DIRECTORY / "2.11.1" / "source.grb")
    asset_2_11_2 = GerberX3Asset(THIS_DIRECTORY / "2.11.2" / "source.grb")
    asset_4_4_6 = GerberX3Asset(THIS_DIRECTORY / "4.4.6" / "source.grb")
    asset_4_9_1 = GerberX3Asset(THIS_DIRECTORY / "4.9.1" / "source.grb")
    asset_4_9_6 = GerberX3Asset(THIS_DIRECTORY / "4.9.6" / "source.grb")
    asset_4_9_6_0 = GerberX3Asset(THIS_DIRECTORY / "4.9.6" / "source_0.grb")
    asset_4_9_6_1 = GerberX3Asset(THIS_DIRECTORY / "4.9.6" / "source_1.grb")
    asset_4_9_6_2 = GerberX3Asset(THIS_DIRECTORY / "4.9.6" / "source_2.grb")
    asset_4_9_6_3 = GerberX3Asset(THIS_DIRECTORY / "4.9.6" / "source_3.grb")
    asset_4_10_4_1 = GerberX3Asset(THIS_DIRECTORY / "4.10.4.1" / "source.grb")
    asset_4_10_4_2 = GerberX3Asset(THIS_DIRECTORY / "4.10.4.2" / "source.grb")
    asset_4_10_4_4 = GerberX3Asset(THIS_DIRECTORY / "4.10.4.4" / "source.grb")
    asset_4_10_4_7 = GerberX3Asset(THIS_DIRECTORY / "4.10.4.7" / "source.grb")
    asset_4_10_4_8 = GerberX3Asset(THIS_DIRECTORY / "4.10.4.8" / "source.grb")
    asset_4_10_4_9 = GerberX3Asset(THIS_DIRECTORY / "4.10.4.9" / "source.grb")
    asset_4_11_4 = GerberX3Asset(THIS_DIRECTORY / "4.11.4" / "source.grb")
