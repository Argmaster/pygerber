from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class MacroCodeAssets(Namespace):
    code_1 = GerberX3Asset(THIS_DIRECTORY / "code_1.grb")
    code_2 = GerberX3Asset(THIS_DIRECTORY / "code_2.grb")
    code_20 = GerberX3Asset(THIS_DIRECTORY / "code_20.grb")
