from __future__ import annotations

import inspect
from pathlib import Path
from typing import ClassVar

import pytest

from pygerber.gerberx3.compiler import Compiler
from pygerber.gerberx3.parser.pyparsing.parser import Parser
from pygerber.vm.pillow.vm import PillowResult, PillowVirtualMachine
from test.assets.asset import GerberX3Asset
from test.assets.gerberx3.A64_OLinuXino_rev_G import A64_OlinuXino_Rev_G
from test.assets.gerberx3.FcPoly_Test import FcPoly_Test
from test.assets.gerberx3.flashes import Flashes

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent

OUTPUT_DUMP_DIRECTORY = THIS_DIRECTORY / f"{THIS_FILE.name}.output"
OUTPUT_DUMP_DIRECTORY.mkdir(exist_ok=True)


class PillowRenderE2E:
    def _render(self, source: GerberX3Asset, dpmm: int = 10) -> PillowResult:
        ast = Parser().parse(source.load())
        rvmc = Compiler().compile(ast)
        return PillowVirtualMachine(dpmm=dpmm).run(rvmc)


def this_func_name() -> str:
    frame = inspect.currentframe()
    if frame is None:
        return ""

    back_frame = frame.f_back
    if back_frame is None:
        return ""

    return back_frame.f_code.co_name


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
