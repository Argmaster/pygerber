from __future__ import annotations

import inspect
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal, Type

import pytest
from PIL import Image

from pygerber.gerber.ast.nodes.file import File
from pygerber.gerber.compiler import compile
from pygerber.gerber.parser import parse
from pygerber.vm import render
from pygerber.vm.shapely.vm import ShapelyResult, ShapelyVirtualMachine
from test.assets.asset import GerberX3Asset
from test.assets.assetlib import ImageAnalyzer, ImageAsset, TextAsset
from test.assets.generated.macro import (
    get_custom_circle_local_2_0,
    get_custom_circle_local_2_0_ring_rot_30,
    get_custom_circle_local_2_0_rot_30,
)
from test.assets.gerberx3 import A64_OLinuXino_rev_G
from test.assets.gerberx3.arc.clockwise import ClockwiseArcAssets
from test.assets.gerberx3.arc.counterclockwise import CounterClockwiseArcAssets
from test.assets.gerberx3.ATMEGA328 import ATMEGA328Assets
from test.assets.gerberx3.FcPoly_Test import FcPoly_Test
from test.assets.gerberx3.flashes import Flashes
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


class ShapelyRender:
    parser: Literal["pyparsing"] = "pyparsing"
    dpmm: int = 20

    def create_image(self, source: str) -> Image.Image:
        from reportlab.graphics import renderPM
        from svglib.svglib import svg2rlg

        ast = parse(source, parser=self.parser)
        rvmc = compile(ast)
        result = render(rvmc, backend="shapely")

        with TemporaryDirectory() as tempdir:
            svg_path = Path(tempdir) / "tmp.svg"
            png_path = Path(tempdir) / "tmp.png"

            result.save(svg_path, file_format="SVG")

            drawing = svg2rlg(svg_path.as_posix())
            assert drawing is not None

            renderPM.drawToFile(
                drawing,
                png_path.as_posix(),
                fmt="PNG",
                dpi=(self.dpmm * 25.4),
            )
            img = Image.open(png_path.as_posix(), formats=["png"])
            # Pillow images are lazy-loaded and since we are using temporary directory
            # we have to load image before temp dir is deleted.
            img.load()

        return img

    def compare_with_reference(
        self, reference: ImageAsset, ssim_threshold: float, image: Image.Image
    ) -> None:
        ia = ImageAnalyzer(reference.load())
        ia.assert_same_size(image)
        (
            ia.histogram_compare_color(image)
            .assert_channel_count(3)
            .assert_greater_or_equal_values(0.99)
        )
        assert ia.structural_similarity(image) > ssim_threshold


class TestOLinuXinoRevG(ShapelyRender):
    dpmm: int = 40

    @tag(Tag.SHAPELY, Tag.EXTRAS, Tag.OPENCV, Tag.SKIMAGE, Tag.SVGLIB)
    @pytest.mark.parametrize(
        ("asset", "reference", "ssim_threshold"),
        [
            (
                A64_OLinuXino_rev_G.A64_OlinuXino_Rev_G_B_Cu,
                A64_OLinuXino_rev_G.A64_OlinuXino_Rev_G_B_Cu_png_shapely,
                0.99,
            ),
            (
                A64_OLinuXino_rev_G.A64_OlinuXino_Rev_G_F_Cu,
                A64_OLinuXino_rev_G.A64_OlinuXino_Rev_G_F_Cu_png_shapely,
                0.99,
            ),
        ],
        ids=["B_Cu", "F_Cu"],
    )
    def test_render_shapely(
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


class TestFcPolyTest(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_bottom(self) -> None:
        result = self._render(FcPoly_Test.bottom)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top(self) -> None:
        result = self._render(FcPoly_Test.top)
        self._save(result)


class TestFlashes(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_00_circle_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_00_circle_h_4_tbh_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_h_4_tbh_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_00_circle_4_grb(self) -> None:
        result = self._render(Flashes.asset_00_circle_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_01_rectangle_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_01_rectangle_v_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_v_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_01_rectangle_v_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_v_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_01_rectangle_4_grb(self) -> None:
        result = self._render(Flashes.asset_01_rectangle_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_02_obround_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_02_obround_v_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_v_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_02_obround_v_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_v_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_02_obround_4_grb(self) -> None:
        result = self._render(Flashes.asset_02_obround_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_03_polygon3_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_03_polygon3_r90_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_r90_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_03_polygon3_r90_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_r90_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_03_polygon3_4_grb(self) -> None:
        result = self._render(Flashes.asset_03_polygon3_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_04_polygon6_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_04_polygon6_r90_h_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_r90_h_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_04_polygon6_r90_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_r90_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_04_polygon6_4_grb(self) -> None:
        result = self._render(Flashes.asset_04_polygon6_4_grb)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_05_circle_h_rectangle_h_obround_h_triangle_h_grb(self) -> None:
        result = self._render(
            Flashes.asset_05_circle_h_rectangle_h_obround_h_triangle_h_grb
        )
        self._save(result)


class TestFlashesWithTransform(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_30(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_45(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_60(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_60)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_90(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_90)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_45_mirror_x(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45_mirror_x)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_45_mirror_y(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45_mirror_y)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_45_mirror_xy(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_45_mirror_xy)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_30_mirror_x(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30_mirror_x)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_30_mirror_y(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30_mirror_y)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_rectangle_rotation_30_mirror_xy(self) -> None:
        result = self._render(FlashesWithTransform.rectangle_rotation_30_mirror_xy)
        self._save(result)


class TestGeneratedMacro(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_custom_circle_local_2_0(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0())
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_custom_circle_local_2_0_rot_30(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0_rot_30())
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_custom_circle_local_2_0_ring_rot_30(self) -> None:
        result = self._render_ast(get_custom_circle_local_2_0_ring_rot_30())
        self._save(result)


class TestMacroCodes(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_1(self) -> None:
        result = self._render(MacroCodeAssets.code_1)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_2(self) -> None:
        result = self._render(MacroCodeAssets.code_2)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_20(self) -> None:
        result = self._render(MacroCodeAssets.code_20)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_4_0(self) -> None:
        result = self._render(MacroCodeAssets.code_4_0)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_4_1(self) -> None:
        result = self._render(MacroCodeAssets.code_4_1)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_5(self) -> None:
        result = self._render(MacroCodeAssets.code_5)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_6(self) -> None:
        result = self._render(MacroCodeAssets.code_6)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_7_0(self) -> None:
        result = self._render(MacroCodeAssets.code_7_0)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_7_1(self) -> None:
        result = self._render(MacroCodeAssets.code_7_1)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_7_2(self) -> None:
        result = self._render(MacroCodeAssets.code_7_2)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_7_3(self) -> None:
        result = self._render(MacroCodeAssets.code_7_3)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_21(self) -> None:
        result = self._render(MacroCodeAssets.code_21)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_code_22(self) -> None:
        result = self._render(MacroCodeAssets.code_22)
        self._save(result)


class ArcSuite(ShapelyRenderE2E):
    assets: Type[ClockwiseArcAssets] | Type[CounterClockwiseArcAssets]

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_full(self) -> None:
        result = self._render(self.assets.full)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_bot_half(self) -> None:
        result = self._render(self.assets.half_bot)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_half(self) -> None:
        result = self._render(self.assets.half_top)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_left_half(self) -> None:
        result = self._render(self.assets.half_left)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_right_half(self) -> None:
        result = self._render(self.assets.half_right)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_quarter_bot_left(self) -> None:
        result = self._render(self.assets.quarter_bot_left)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_quarter_bot_right(self) -> None:
        result = self._render(self.assets.quarter_bot_right)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_quarter_top_left(self) -> None:
        result = self._render(self.assets.quarter_top_left)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_quarter_top_right(self) -> None:
        result = self._render(self.assets.quarter_top_right)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_three_fourth_bot_left(self) -> None:
        result = self._render(self.assets.three_fourth_bot_left)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_three_fourth_bot_right(self) -> None:
        result = self._render(self.assets.three_fourth_bot_right)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_three_fourth_top_left(self) -> None:
        result = self._render(self.assets.three_fourth_top_left)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_three_fourth_top_right(self) -> None:
        result = self._render(self.assets.three_fourth_top_right)
        self._save(result)


class TestMqClockwiseArcs(ArcSuite):
    assets = ClockwiseArcAssets


class TestMqCounterClockwiseArcs(ArcSuite):
    assets = CounterClockwiseArcAssets


class TestGerberSpecExampleAssets(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_2_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_1)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_2_11_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_11_1)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_2_11_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_2_11_2)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_4_6(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_4_6)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_9_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_1)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_9_6(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_9_6_0(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_0)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_9_6_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_1)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_9_6_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_2)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_9_6_3(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_9_6_3)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_10_4_1(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_1)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_10_4_2(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_2)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_10_4_4(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_4)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_10_4_7(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_7)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_10_4_8(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_8)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_10_4_9(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_10_4_9)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_asset_4_11_4(self) -> None:
        result = self._render(GerberSpecExampleAssets.asset_4_11_4)
        self._save(result)


class TestATMEGA328(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_bottom_copper(self) -> None:
        result = self._render(ATMEGA328Assets.bottom_copper)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_bottom_mask(self) -> None:
        result = self._render(ATMEGA328Assets.bottom_mask)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_bottom_paste(self) -> None:
        result = self._render(ATMEGA328Assets.bottom_paste)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_bottom_silk(self) -> None:
        result = self._render(ATMEGA328Assets.bottom_silk)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_edge_cuts(self) -> None:
        result = self._render(ATMEGA328Assets.edge_cuts)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_copper(self) -> None:
        result = self._render(ATMEGA328Assets.top_copper)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_mask(self) -> None:
        result = self._render(ATMEGA328Assets.top_mask)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_paste(self) -> None:
        result = self._render(ATMEGA328Assets.top_paste)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_silk(self) -> None:
        result = self._render(ATMEGA328Assets.top_silk)
        self._save(result)


class TestPolarityCutouts(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_sample(self) -> None:
        result = self._render(PolarityCutouts.sample)
        self._save(result)


class TestKiCadGerberX2(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_bottom_copper(self) -> None:
        result = self._render(KiCadGerberX2Assets.bottom_copper)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_bottom_mask(self) -> None:
        result = self._render(KiCadGerberX2Assets.bottom_mask)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_edge_cuts(self) -> None:
        result = self._render(KiCadGerberX2Assets.edge_cuts)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_copper(self) -> None:
        result = self._render(KiCadGerberX2Assets.top_copper)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_mask(self) -> None:
        result = self._render(KiCadGerberX2Assets.top_mask)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_paste(self) -> None:
        result = self._render(KiCadGerberX2Assets.top_paste)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_top_silk(self) -> None:
        result = self._render(KiCadGerberX2Assets.top_silk)
        self._save(result)


class TestStepAndRepeat(ShapelyRenderE2E):
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_x_3(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_x_3)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_x_6(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_x_6)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_y_3(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_y_3)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_y_6(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_y_6)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_xy_3_6(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_3_6)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_xy_6_6(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_6_6)
        self._save(result)

    # Rot 30

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_x_3_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_x_3_rot_30)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_x_6_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_x_6_rot_30)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_y_3_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_y_3_rot_30)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_y_6_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_y_6_rot_30)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_xy_3_6_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_3_6_rot_30)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_xy_6_6_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_6_6_rot_30)
        self._save(result)

    # Line

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_xy_2_2_line(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_2_2_line)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_xy_2_2_line_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_2_2_line_rot_30)
        self._save(result)

    # AB

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_xy_2_2_ab(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_2_2_ab)
        self._save(result)

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_cr_xy_2_2_ab_rot_30(self) -> None:
        result = self._render(StepAndRepeatAssets.cr_xy_2_2_ab_rot_30)
        self._save(result)
