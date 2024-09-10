from __future__ import annotations

import inspect
from pathlib import Path
from typing import ClassVar

import pytest

from pygerber.gerberx3.ast.nodes import File
from pygerber.gerberx3.compiler import Compiler
from pygerber.gerberx3.parser.pyparsing.parser import Parser
from pygerber.vm.pillow.vm import PillowResult, PillowVirtualMachine
from test.assets.asset import GerberX3Asset
from test.assets.generated.macro import (
    get_custom_circle_local_2_0,
    get_custom_circle_local_2_0_ring_rot_30,
    get_custom_circle_local_2_0_rot_30,
)
from test.assets.gerberx3.A64_OLinuXino_rev_G import A64_OlinuXino_Rev_G
from test.assets.gerberx3.FcPoly_Test import FcPoly_Test
from test.assets.gerberx3.flashes import Flashes
from test.assets.gerberx3.flashes_with_transform import FlashesWithTransform
from test.assets.gerberx3.macro.codes import MacroCodeAssets

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent

OUTPUT_DUMP_DIRECTORY = THIS_DIRECTORY / f"{THIS_FILE.name}.output"
OUTPUT_DUMP_DIRECTORY.mkdir(exist_ok=True)


class PillowRenderE2E:
    def _render(self, source: GerberX3Asset, dpmm: int = 10) -> PillowResult:
        ast = Parser().parse(source.load())
        return self._render_ast(ast, dpmm=dpmm)

    def _render_ast(self, ast: File, dpmm: int = 10) -> PillowResult:
        rvmc = Compiler().compile(ast)
        return PillowVirtualMachine(dpmm=dpmm).run(rvmc)

    def _save(self, result: PillowResult) -> None:
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name(up=2)}.png")


def this_func_name(up: int = 1) -> str:
    return inspect.stack()[up].function


class TestOLinuXinoRevG(PillowRenderE2E):
    @pytest.mark.skip("Not implemented")
    def test_bottom_copper(self) -> None:
        result = self._render(A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Cu, dpmm=100)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    @pytest.mark.skip("Not implemented")
    def test_bottom_mask(self) -> None:
        result = self._render(A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Mask, dpmm=100)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    @pytest.mark.skip("Not implemented")
    def test_bottom_paste(self) -> None:
        result = self._render(A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Paste, dpmm=100)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")


class TestFcPolyTest(PillowRenderE2E):
    def test_bottom(self) -> None:
        result = self._render(FcPoly_Test.bottom, dpmm=5000)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_top(self) -> None:
        result = self._render(FcPoly_Test.top, dpmm=5000)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")


class TestFlashes(PillowRenderE2E):
    DPMM: ClassVar[int] = 50

    def test_00_circle_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_00_circle_h_4_tbh_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_h_4_tbh_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_00_circle_4_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_01_rectangle_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_01_rectangle_v_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_v_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_01_rectangle_v_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_v_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_01_rectangle_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_02_obround_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_02_obround_v_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_v_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_02_obround_v_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_v_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_02_obround_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_03_polygon3_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_03_polygon3_r90_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_r90_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_03_polygon3_r90_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_r90_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_03_polygon3_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_04_polygon6_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_04_polygon6_r90_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_r90_h_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_04_polygon6_r90_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_r90_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_04_polygon6_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_4_grb, dpmm=self.DPMM)
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")

    def test_05_circle_h_rectangle_h_obround_h_triangle_h_grb(self) -> None:
        result = self._render(
            Flashes.asset_05_circle_h_rectangle_h_obround_h_triangle_h_grb,
            dpmm=self.DPMM,
        )
        result.get_image().save(OUTPUT_DUMP_DIRECTORY / f"{this_func_name()}.png")


class TestFlashesWithTransform(PillowRenderE2E):
    def test_rectangle_rotation_30(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30, dpmm=30)
        self._save(result)

    def test_rectangle_rotation_45(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45, dpmm=30)
        self._save(result)

    def test_rectangle_rotation_60(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_60, dpmm=30)
        self._save(result)

    def test_rectangle_rotation_90(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_90, dpmm=30)
        self._save(result)

    def test_rectangle_rotation_45_mirror_x(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_45_mirror_x, dpmm=30
        )
        self._save(result)

    def test_rectangle_rotation_45_mirror_y(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_45_mirror_y, dpmm=30
        )
        self._save(result)

    def test_rectangle_rotation_45_mirror_xy(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_45_mirror_xy, dpmm=30
        )
        self._save(result)

    def test_rectangle_rotation_30_mirror_x(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_30_mirror_x, dpmm=30
        )
        self._save(result)

    def test_rectangle_rotation_30_mirror_y(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_30_mirror_y, dpmm=30
        )
        self._save(result)

    def test_rectangle_rotation_30_mirror_xy(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_30_mirror_xy, dpmm=30
        )
        self._save(result)


class TestGeneratedMacro(PillowRenderE2E):
    def test_custom_circle_local_2_0(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0(), 100)
        self._save(result)

    def test_custom_circle_local_2_0_rot_30(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0_rot_30(), 100)
        self._save(result)

    def test_custom_circle_local_2_0_ring_rot_30(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0_ring_rot_30(), 100)
        self._save(result)


class TestMacroCodes(PillowRenderE2E):
    def test_code_1(self) -> None:
        result = self._render(MacroCodeAssets.code_1, dpmm=100)
        self._save(result)

    def test_code_2(self) -> None:
        result = self._render(MacroCodeAssets.code_2, dpmm=50)
        self._save(result)

    def test_code_20(self) -> None:
        result = self._render(MacroCodeAssets.code_20, dpmm=50)
        self._save(result)

    def test_code_4_0(self) -> None:
        result = self._render(MacroCodeAssets.code_4_0, dpmm=50)
        self._save(result)

    def test_code_4_1(self) -> None:
        result = self._render(MacroCodeAssets.code_4_1, dpmm=10000)
        self._save(result)
