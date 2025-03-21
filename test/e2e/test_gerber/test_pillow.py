from __future__ import annotations

import inspect
from io import BytesIO
from pathlib import Path
from typing import ClassVar, Literal, Type

import pytest
from PIL import Image

import test.assets.gerberx3.A64_OLinuXino_rev_G as A64_OlinuXino_Rev_G
from pygerber.gerber.ast.nodes import File
from pygerber.gerber.compiler import compile
from pygerber.gerber.parser import parse
from pygerber.gerber.parser.pyparsing.parser import Parser
from pygerber.vm import render
from pygerber.vm.pillow.vm import PillowResult, PillowVirtualMachine
from test.assets.asset import GerberX3Asset
from test.assets.assetlib import ImageAnalyzer, ImageAsset, TextAsset
from test.assets.generated.macro import (
    get_custom_circle_local_2_0,
    get_custom_circle_local_2_0_ring_rot_30,
    get_custom_circle_local_2_0_rot_30,
)
from test.assets.gerberx3 import flashes
from test.assets.gerberx3.arc.clockwise import ClockwiseArcAssets
from test.assets.gerberx3.arc.counterclockwise import CounterClockwiseArcAssets
from test.assets.gerberx3.ATMEGA328 import ATMEGA328Assets
from test.assets.gerberx3.FcPoly_Test import FcPoly_Test
from test.assets.gerberx3.flashes_with_transform import FlashesWithTransform
from test.assets.gerberx3.KicadGerberX2 import KiCadGerberX2Assets
from test.assets.gerberx3.macro.codes import MacroCodeAssets
from test.assets.gerberx3.polarity_cutouts import PolarityCutouts
from test.assets.gerberx3.step_and_repeat import StepAndRepeatAssets
from test.assets.gerberx3.ucamco import GerberSpecExampleAssets
from test.tags import Tag, tag

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent

OUTPUT_DUMP_DIRECTORY = THIS_DIRECTORY / f"{THIS_FILE.name}.output"
OUTPUT_DUMP_DIRECTORY.mkdir(exist_ok=True)


class PillowRenderE2E:
    def _render(self, source: GerberX3Asset, dpmm: int = 10) -> PillowResult:
        ast = Parser().parse(source.load())
        return self._render_ast(ast, dpmm=dpmm)

    def _render_ast(self, ast: File, dpmm: int = 10) -> PillowResult:
        rvmc = compile(ast)
        return PillowVirtualMachine(dpmm=dpmm).run(rvmc)

    def _save(self, result: PillowResult) -> None:
        caller_frame = inspect.stack()[1]
        caller_function_name = caller_frame.function
        caller_self = caller_frame.frame.f_locals.get("self")

        if caller_self is not None:
            dump_directory = OUTPUT_DUMP_DIRECTORY / caller_self.__class__.__name__
            dump_directory.mkdir(exist_ok=True, parents=True)
        else:
            dump_directory = OUTPUT_DUMP_DIRECTORY

        result.get_image_no_style().save(dump_directory / f"{caller_function_name}.png")


class PillowRenderNewE2E:
    parser: Literal["pyparsing"] = "pyparsing"
    dpmm: int = 20

    def create_image(self, source: str) -> Image.Image:
        ast = parse(source, parser=self.parser)
        rvmc = compile(ast)
        result = render(rvmc, dpmm=self.dpmm)

        buffer = BytesIO()
        result.save(buffer, file_format="PNG")

        buffer.seek(0)
        return Image.open(buffer, formats=["png"])

    def compare_with_reference(
        self, reference: ImageAsset, ssim_threshold: float, image: Image.Image
    ) -> None:
        ia = ImageAnalyzer(reference.load())
        ia.assert_same_size(image)
        (
            ia.histogram_compare_color(image)
            .assert_channel_count(4)
            .assert_greater_or_equal_values(0.99)
        )
        assert ia.structural_similarity(image) > ssim_threshold

    def compare_with_reference_exact(
        self, reference: ImageAsset, image: Image.Image
    ) -> None:
        ia = ImageAnalyzer(reference.load())
        assert ia.exact_match(image)


class TestOLinuXinoRevG(PillowRenderNewE2E):
    dpmm: int = 40

    @tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
    @pytest.mark.parametrize(
        ("asset", "reference", "ssim_threshold"),
        [
            (
                A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Cu,
                A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_B_Cu_png,
                0.99,
            ),
            (
                A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_F_Cu,
                A64_OlinuXino_Rev_G.A64_OlinuXino_Rev_G_F_Cu_png,
                0.99,
            ),
        ],
        ids=["B_Cu", "F_Cu"],
    )
    def test_render_pillow(
        self,
        asset: TextAsset,
        reference: ImageAsset,
        ssim_threshold: float,
        *,
        is_regeneration_enabled: bool,
    ) -> None:
        image = self.create_image(asset.load())
        if is_regeneration_enabled:
            reference.update(image)
        else:
            self.compare_with_reference(reference, ssim_threshold, image)


class TestFcPolyTest(PillowRenderE2E):
    @tag(Tag.PILLOW)
    def test_bottom(self) -> None:
        result = self._render(FcPoly_Test.bottom, dpmm=5000)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top(self) -> None:
        result = self._render(FcPoly_Test.top, dpmm=5000)
        self._save(result)


class TestFlashes(PillowRenderNewE2E):
    DPMM: ClassVar[int] = 50

    @tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
    @pytest.mark.parametrize(
        ("asset", "reference"),
        [
            (
                flashes.asset_00_circle_h_4_grb,
                flashes.asset_00_circle_h_4_grb_png,
            ),
            (
                flashes.asset_00_circle_4_grb,
                flashes.asset_00_circle_4_grb_png,
            ),
            (
                flashes.asset_00_circle_h_4_tbh_grb,
                flashes.asset_00_circle_h_4_tbh_grb_png,
            ),
            (
                flashes.asset_00_circle_4_node_finder_grb,
                flashes.asset_00_circle_4_node_finder_grb_png,
            ),
            (
                flashes.asset_01_rectangle_h_4_grb,
                flashes.asset_01_rectangle_h_4_grb_png,
            ),
            (
                flashes.asset_01_rectangle_v_h_4_grb,
                flashes.asset_01_rectangle_v_h_4_grb_png,
            ),
            (
                flashes.asset_01_rectangle_v_4_grb,
                flashes.asset_01_rectangle_v_4_grb_png,
            ),
            (
                flashes.asset_01_rectangle_4_grb,
                flashes.asset_01_rectangle_4_grb_png,
            ),
            (
                flashes.asset_02_obround_h_4_grb,
                flashes.asset_02_obround_h_4_grb_png,
            ),
            (
                flashes.asset_02_obround_v_h_4_grb,
                flashes.asset_02_obround_v_h_4_grb_png,
            ),
            (
                flashes.asset_02_obround_v_4_grb,
                flashes.asset_02_obround_v_4_grb_png,
            ),
            (
                flashes.asset_02_obround_4_grb,
                flashes.asset_02_obround_4_grb_png,
            ),
            (
                flashes.asset_03_polygon3_h_4_grb,
                flashes.asset_03_polygon3_h_4_grb_png,
            ),
            (
                flashes.asset_03_polygon3_r90_h_4_grb,
                flashes.asset_03_polygon3_r90_h_4_grb_png,
            ),
            (
                flashes.asset_03_polygon3_r90_4_grb,
                flashes.asset_03_polygon3_r90_4_grb_png,
            ),
            (
                flashes.asset_03_polygon3_4_grb,
                flashes.asset_03_polygon3_4_grb_png,
            ),
            (
                flashes.asset_04_polygon6_h_4_grb,
                flashes.asset_04_polygon6_h_4_grb_png,
            ),
            (
                flashes.asset_04_polygon6_r90_h_4_grb,
                flashes.asset_04_polygon6_r90_h_4_grb_png,
            ),
            (
                flashes.asset_04_polygon6_r90_4_grb,
                flashes.asset_04_polygon6_r90_4_grb_png,
            ),
            (
                flashes.asset_04_polygon6_4_grb,
                flashes.asset_04_polygon6_4_grb_png,
            ),
            (
                flashes.asset_05_circle_h_rectangle_h_obround_h_triangle_h_grb,
                flashes.asset_05_circle_h_rectangle_h_obround_h_triangle_h_grb_png,
            ),
        ],
        ids=[
            "00_circle_h_4",
            "00_circle_4",
            "00_circle_h_4_tbh",
            "00_circle_4_node_finder",
            "01_rectangle_h_4",
            "01_rectangle_v_h_4",
            "01_rectangle_v_4",
            "01_rectangle_4",
            "02_obround_h_4",
            "02_obround_v_h_4",
            "02_obround_v_4",
            "02_obround_4",
            "03_polygon3_h_4",
            "03_polygon3_r90_h_4",
            "03_polygon3_r90_4",
            "03_polygon3_4",
            "04_polygon6_h_4",
            "04_polygon6_r90_h_4",
            "04_polygon6_r90_4",
            "04_polygon6_4",
            "05_circle_h_rectangle_h_obround_h_triangle_h",
        ],
    )
    def test_render_pillow(
        self,
        asset: TextAsset,
        reference: ImageAsset,
        *,
        is_regeneration_enabled: bool,
    ) -> None:
        image = self.create_image(asset.load())
        if is_regeneration_enabled:
            reference.update(image)
        else:
            self.compare_with_reference_exact(reference, image)


class TestFlashesWithTransform(PillowRenderE2E):
    @tag(Tag.PILLOW)
    def test_rectangle_rotation_30(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30, dpmm=30)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_45(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45, dpmm=30)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_60(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_60, dpmm=30)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_90(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_90, dpmm=30)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_45_mirror_x(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_45_mirror_x, dpmm=30
        )
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_45_mirror_y(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_45_mirror_y, dpmm=30
        )
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_45_mirror_xy(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_45_mirror_xy, dpmm=30
        )
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_30_mirror_x(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_30_mirror_x, dpmm=30
        )
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_30_mirror_y(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_30_mirror_y, dpmm=30
        )
        self._save(result)

    @tag(Tag.PILLOW)
    def test_rectangle_rotation_30_mirror_xy(self) -> None:
        result = self._render(
            FlashesWithTransform.rectangle_rotation_30_mirror_xy, dpmm=30
        )
        self._save(result)


class TestGeneratedMacro(PillowRenderE2E):
    @tag(Tag.PILLOW)
    def test_custom_circle_local_2_0(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0(), 100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_custom_circle_local_2_0_rot_30(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0_rot_30(), 100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_custom_circle_local_2_0_ring_rot_30(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0_ring_rot_30(), 100)
        self._save(result)


class TestMacroCodes(PillowRenderE2E):
    @tag(Tag.PILLOW)
    def test_code_1(self) -> None:
        result = self._render(MacroCodeAssets.code_1, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_2(self) -> None:
        result = self._render(MacroCodeAssets.code_2, dpmm=50)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_20(self) -> None:
        result = self._render(MacroCodeAssets.code_20, dpmm=50)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_4_0(self) -> None:
        result = self._render(MacroCodeAssets.code_4_0, dpmm=50)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_4_1(self) -> None:
        result = self._render(MacroCodeAssets.code_4_1, dpmm=10000)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_5(self) -> None:
        result = self._render(MacroCodeAssets.code_5, dpmm=50)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_6(self) -> None:
        result = self._render(MacroCodeAssets.code_6, dpmm=50)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_7_0(self) -> None:
        result = self._render(MacroCodeAssets.code_7_0, dpmm=200)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_7_1(self) -> None:
        result = self._render(MacroCodeAssets.code_7_1, dpmm=200)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_7_2(self) -> None:
        result = self._render(MacroCodeAssets.code_7_2, dpmm=200)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_7_3(self) -> None:
        result = self._render(MacroCodeAssets.code_7_3, dpmm=200)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_21(self) -> None:
        result = self._render(MacroCodeAssets.code_21, dpmm=200)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_code_22(self) -> None:
        result = self._render(MacroCodeAssets.code_22, dpmm=200)
        self._save(result)


class ArcSuite(PillowRenderE2E):
    assets: Type[ClockwiseArcAssets] | Type[CounterClockwiseArcAssets]
    dpmm = 20

    @tag(Tag.PILLOW)
    def test_full(self) -> None:
        result = self._render(self.assets.full, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_bot_half(self) -> None:
        result = self._render(self.assets.half_bot, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_half(self) -> None:
        result = self._render(self.assets.half_top, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_left_half(self) -> None:
        result = self._render(self.assets.half_left, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_right_half(self) -> None:
        result = self._render(self.assets.half_right, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_quarter_bot_left(self) -> None:
        result = self._render(self.assets.quarter_bot_left, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_quarter_bot_right(self) -> None:
        result = self._render(self.assets.quarter_bot_right, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_quarter_top_left(self) -> None:
        result = self._render(self.assets.quarter_top_left, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_quarter_top_right(self) -> None:
        result = self._render(self.assets.quarter_top_right, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_three_fourth_bot_left(self) -> None:
        result = self._render(self.assets.three_fourth_bot_left, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_three_fourth_bot_right(self) -> None:
        result = self._render(self.assets.three_fourth_bot_right, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_three_fourth_top_left(self) -> None:
        result = self._render(self.assets.three_fourth_top_left, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_three_fourth_top_right(self) -> None:
        result = self._render(self.assets.three_fourth_top_right, dpmm=self.dpmm)
        self._save(result)


class TestMqClockwiseArcs(ArcSuite):
    assets = ClockwiseArcAssets


class TestMqCounterClockwiseArcs(ArcSuite):
    assets = CounterClockwiseArcAssets


class TestGerberSpecExampleAssets(PillowRenderE2E):
    @tag(Tag.PILLOW)
    def test_asset_2_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_1, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_2_11_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_11_1, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_2_11_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_11_2, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_4_6(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_4_6, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_9_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_1, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_9_6(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_9_6_0(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_0, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_9_6_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_1, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_9_6_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_2, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_9_6_3(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_3, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_10_4_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_1, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_10_4_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_2, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_10_4_4(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_4, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_10_4_7(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_7, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_10_4_8(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_8, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_10_4_9(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_9, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_asset_4_11_4(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_11_4, dpmm=10)
        self._save(result)


class TestATMEGA328(PillowRenderE2E):
    dpmm = 100

    @tag(Tag.PILLOW)
    def test_bottom_copper(self) -> None:
        result = self._render(ATMEGA328Assets.bottom_copper, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_bottom_mask(self) -> None:
        result = self._render(ATMEGA328Assets.bottom_mask, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_bottom_paste(self) -> None:
        result = self._render(ATMEGA328Assets.bottom_paste, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_bottom_silk(self) -> None:
        result = self._render(ATMEGA328Assets.bottom_silk, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_edge_cuts(self) -> None:
        result = self._render(ATMEGA328Assets.edge_cuts, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_copper(self) -> None:
        result = self._render(ATMEGA328Assets.top_copper, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_mask(self) -> None:
        result = self._render(ATMEGA328Assets.top_mask, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_paste(self) -> None:
        result = self._render(ATMEGA328Assets.top_paste, dpmm=self.dpmm)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_silk(self) -> None:
        result = self._render(ATMEGA328Assets.top_silk, dpmm=self.dpmm)
        self._save(result)


class TestPolarityCutouts(PillowRenderE2E):
    @tag(Tag.PILLOW)
    def test_sample(self) -> None:
        result = self._render(PolarityCutouts.sample, dpmm=100)
        self._save(result)


class TestKiCadGerberX2(PillowRenderE2E):
    @tag(Tag.PILLOW)
    def test_bottom_copper(self) -> None:
        result = self._render(KiCadGerberX2Assets.bottom_copper, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_bottom_mask(self) -> None:
        result = self._render(KiCadGerberX2Assets.bottom_mask, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_edge_cuts(self) -> None:
        result = self._render(KiCadGerberX2Assets.edge_cuts, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_copper(self) -> None:
        result = self._render(KiCadGerberX2Assets.top_copper, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_mask(self) -> None:
        result = self._render(KiCadGerberX2Assets.top_mask, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_paste(self) -> None:
        result = self._render(KiCadGerberX2Assets.top_paste, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_top_silk(self) -> None:
        result = self._render(KiCadGerberX2Assets.top_silk, dpmm=100)
        self._save(result)


class TestStepAndRepeat(PillowRenderE2E):
    @tag(Tag.PILLOW)
    def test_cr_x_3(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_x_3, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_x_6(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_x_6, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_y_3(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_y_3, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_y_6(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_y_6, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_xy_3_6(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_3_6, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_xy_6_6(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_6_6, dpmm=100)
        self._save(result)

    # Rot 30

    @tag(Tag.PILLOW)
    def test_cr_x_3_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_x_3_rot_30, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_x_6_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_x_6_rot_30, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_y_3_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_y_3_rot_30, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_y_6_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_y_6_rot_30, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_xy_3_6_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_3_6_rot_30, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_xy_6_6_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_6_6_rot_30, dpmm=100)
        self._save(result)

    # Line

    @tag(Tag.PILLOW)
    def test_cr_xy_2_2_line(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_2_2_line, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_xy_2_2_line_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_2_2_line_rot_30, dpmm=100)
        self._save(result)

    # AB

    @tag(Tag.PILLOW)
    def test_cr_xy_2_2_ab(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_2_2_ab, dpmm=100)
        self._save(result)

    @tag(Tag.PILLOW)
    def test_cr_xy_2_2_ab_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_2_2_ab_rot_30, dpmm=100)
        self._save(result)
