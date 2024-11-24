from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import test.assets.gerberx3.A64_OLinuXino_rev_G as A64_OlinuXino_Rev_G
from test.assets.gerberx3.ATMEGA328 import ATMEGA328Assets
from test.assets.gerberx3.FcPoly_Test import FcPoly_Test
from test.assets.gerberx3.step_and_repeat import StepAndRepeatAssets
from test.assets.gerberx3.ucamco import GerberSpecExampleAssets

from pygerber.gerber.optimizer.optimizer_pass.base_pass import BasePass
from pygerber.gerber.parser import parse

if TYPE_CHECKING:
    from test.assets.asset import GerberX3Asset


@pytest.mark.parametrize(
    "example",
    [
        FcPoly_Test.bottom,
        ATMEGA328Assets.bottom_copper,
        A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Cu,
        StepAndRepeatAssets.cr_xy_2_2_line_rot_30,
        GerberSpecExampleAssets.asset_2_11_1,
    ],
    ids=str,
)
def test_base_pass_keep_file_structure(example: GerberX3Asset) -> None:
    ast = parse(example.load())
    result = BasePass().optimize(ast)

    if result.model_dump_json() != ast.model_dump_json():
        raise AssertionError
