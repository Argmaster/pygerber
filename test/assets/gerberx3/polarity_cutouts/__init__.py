from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class PolarityCutouts(Namespace):
    sample = GerberX3Asset(THIS_DIRECTORY / "sample.grb")
