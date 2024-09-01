from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Assert

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class FcPoly_Test(Namespace):  # noqa: N801
    bottom = GerberX3Assert(THIS_DIRECTORY / "bottom.grb")
    top = GerberX3Assert(THIS_DIRECTORY / "top.grb")
