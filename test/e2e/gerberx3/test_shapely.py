from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from pygerber.gerber.ast.nodes.file import File
from pygerber.gerber.compiler import compile
from pygerber.gerber.parser import parse
from pygerber.vm.shapely.vm import ShapelyResult, ShapelyVirtualMachine
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
from test.assets.gerberx3.ucamco import GerberSpecExampleAssets

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent

OUTPUT_DUMP_DIRECTORY = THIS_DIRECTORY / f"{THIS_FILE.name}.output"
OUTPUT_DUMP_DIRECTORY.mkdir(exist_ok=True)


class ShapelyRenderE2E:
    def _render(self, source: GerberX3Asset) -> ShapelyResult:
        ast = parse(source.load())
        return self._render_ast(ast)

    def _render_ast(self, ast: File) -> ShapelyResult:
        rvmc = compile(ast)
        return ShapelyVirtualMachine().run(rvmc)

    def _save(self, result: ShapelyResult) -> None:
        caller_frame = inspect.stack()[1]
        caller_function_name = caller_frame.function
        caller_self = caller_frame.frame.f_locals.get("self")

        if caller_self is not None:
            dump_directory = OUTPUT_DUMP_DIRECTORY / caller_self.__class__.__name__
            dump_directory.mkdir(exist_ok=True, parents=True)
        else:
            dump_directory = OUTPUT_DUMP_DIRECTORY

        result.save_svg((dump_directory / caller_function_name).with_suffix(".svg"))


class TestOLinuXinoRevG(ShapelyRenderE2E):
    @pytest.mark.skip("Poor performance skip")
    def test_bottom_copper(self) -> None:
        result = self._render(A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Cu)
        self._save(result)

    def test_bottom_mask(self) -> None:
        result = self._render(A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Mask)
        self._save(result)

    def test_bottom_paste(self) -> None:
        result = self._render(A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Paste)
        self._save(result)


class TestFcPolyTest(ShapelyRenderE2E):
    def test_bottom(self) -> None:
        result = self._render(FcPoly_Test.bottom)
        self._save(result)

    def test_top(self) -> None:
        result = self._render(FcPoly_Test.top)
        self._save(result)


class TestFlashes(ShapelyRenderE2E):
    def test_00_circle_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_h_4_grb)
        self._save(result)

    def test_00_circle_h_4_tbh_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_h_4_tbh_grb)
        self._save(result)

    def test_00_circle_4_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_4_grb)
        self._save(result)

    def test_01_rectangle_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_h_4_grb)
        self._save(result)

    def test_01_rectangle_v_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_v_h_4_grb)
        self._save(result)

    def test_01_rectangle_v_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_v_4_grb)
        self._save(result)

    def test_01_rectangle_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_4_grb)
        self._save(result)

    def test_02_obround_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_h_4_grb)
        self._save(result)

    def test_02_obround_v_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_v_h_4_grb)
        self._save(result)

    def test_02_obround_v_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_v_4_grb)
        self._save(result)

    def test_02_obround_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_4_grb)
        self._save(result)

    def test_03_polygon3_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_h_4_grb)
        self._save(result)

    def test_03_polygon3_r90_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_r90_h_4_grb)
        self._save(result)

    def test_03_polygon3_r90_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_r90_4_grb)
        self._save(result)

    def test_03_polygon3_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_4_grb)
        self._save(result)

    def test_04_polygon6_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_h_4_grb)
        self._save(result)

    def test_04_polygon6_r90_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_r90_h_4_grb)
        self._save(result)

    def test_04_polygon6_r90_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_r90_4_grb)
        self._save(result)

    def test_04_polygon6_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_4_grb)
        self._save(result)

    def test_05_circle_h_rectangle_h_obround_h_triangle_h_grb(self) -> None:
        result = self._render(
            Flashes.asset_05_circle_h_rectangle_h_obround_h_triangle_h_grb
        )
        self._save(result)


class TestFlashesWithTransform(ShapelyRenderE2E):
    def test_rectangle_rotation_30(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30)
        self._save(result)

    def test_rectangle_rotation_45(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45)
        self._save(result)

    def test_rectangle_rotation_60(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_60)
        self._save(result)

    def test_rectangle_rotation_90(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_90)
        self._save(result)

    def test_rectangle_rotation_45_mirror_x(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45_mirror_x)
        self._save(result)

    def test_rectangle_rotation_45_mirror_y(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45_mirror_y)
        self._save(result)

    def test_rectangle_rotation_45_mirror_xy(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45_mirror_xy)
        self._save(result)

    def test_rectangle_rotation_30_mirror_x(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30_mirror_x)
        self._save(result)

    def test_rectangle_rotation_30_mirror_y(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30_mirror_y)
        self._save(result)

    def test_rectangle_rotation_30_mirror_xy(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30_mirror_xy)
        self._save(result)


class TestGeneratedMacro(ShapelyRenderE2E):
    def test_custom_circle_local_2_0(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0())
        self._save(result)

    def test_custom_circle_local_2_0_rot_30(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0_rot_30())
        self._save(result)

    def test_custom_circle_local_2_0_ring_rot_30(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0_ring_rot_30())
        self._save(result)


class TestMacroCodes(ShapelyRenderE2E):
    def test_code_1(self) -> None:
        result = self._render(MacroCodeAssets.code_1)
        self._save(result)

    def test_code_2(self) -> None:
        result = self._render(MacroCodeAssets.code_2)
        self._save(result)

    def test_code_20(self) -> None:
        result = self._render(MacroCodeAssets.code_20)
        self._save(result)

    def test_code_4_0(self) -> None:
        result = self._render(MacroCodeAssets.code_4_0)
        self._save(result)

    def test_code_4_1(self) -> None:
        result = self._render(MacroCodeAssets.code_4_1)
        self._save(result)

    def test_code_5(self) -> None:
        result = self._render(MacroCodeAssets.code_5)
        self._save(result)

    def test_code_6(self) -> None:
        result = self._render(MacroCodeAssets.code_6)
        self._save(result)

    def test_code_7_0(self) -> None:
        result = self._render(MacroCodeAssets.code_7_0)
        self._save(result)

    def test_code_7_1(self) -> None:
        result = self._render(MacroCodeAssets.code_7_1)
        self._save(result)

    def test_code_7_2(self) -> None:
        result = self._render(MacroCodeAssets.code_7_2)
        self._save(result)

    def test_code_7_3(self) -> None:
        result = self._render(MacroCodeAssets.code_7_3)
        self._save(result)

    def test_code_21(self) -> None:
        result = self._render(MacroCodeAssets.code_21)
        self._save(result)

    def test_code_22(self) -> None:
        result = self._render(MacroCodeAssets.code_22)
        self._save(result)


class TestGerberSpecExampleAssets(ShapelyRenderE2E):
    def test_asset_2_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_1)
        self._save(result)

    def test_asset_2_11_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_11_1)
        self._save(result)

    def test_asset_2_11_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_11_2)
        self._save(result)

    def test_asset_4_4_6(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_4_6)
        self._save(result)

    def test_asset_4_9_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_1)
        self._save(result)

    def test_asset_4_9_6(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6)
        self._save(result)

    def test_asset_4_9_6_0(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_0)
        self._save(result)

    def test_asset_4_9_6_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_1)
        self._save(result)

    def test_asset_4_9_6_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_2)
        self._save(result)

    def test_asset_4_9_6_3(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_3)
        self._save(result)

    def test_asset_4_10_4_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_1)
        self._save(result)

    def test_asset_4_10_4_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_2)
        self._save(result)

    def test_asset_4_10_4_4(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_4)
        self._save(result)

    def test_asset_4_10_4_7(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_7)
        self._save(result)

    def test_asset_4_10_4_8(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_8)
        self._save(result)

    def test_asset_4_10_4_9(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_9)
        self._save(result)

    def test_asset_4_11_4(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_11_4)
        self._save(result)
