# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from pathlib import Path
from unittest import TestCase, main

from pygerber.API3D import render_file, render_file_and_save
from pygerber.parser.blender.parser import ParserWithBlender

TESTS_FOLDER = Path(__file__).parent.parent
RENDERED_PATH = TESTS_FOLDER / Path("gerber/rendered")
GERBER_PATH = TESTS_FOLDER / Path("gerber")


class TestBlenderParser(TestCase):

    SOURCE_0 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            M02*
            """

    def test_parser_string(self):
        parser = ParserWithBlender()
        parser.parse(self.SOURCE_0)
        # to manually validate output uncomment this:
        # image.show()
        # to create new comparison image uncomment this:
        parser.save(RENDERED_PATH / "blender" / "SOURCE_0.glb")

    def test_render_file_and_save(self):
        render_file_and_save(
            GERBER_PATH / "s0.grb", RENDERED_PATH / "blender" / "s0_0.glb"
        )

    def render_file_and_optional_save(
        self, filename: str, save: bool = False, **kwargs
    ):
        if save:
            render_file_and_save(
                GERBER_PATH / filename,
                RENDERED_PATH / "blender" / (filename.split(".")[0] + ".blend"),
                **kwargs,
            )
        else:
            render_file(
                GERBER_PATH / filename,
                **kwargs,
            )

    def test_parser_file_0(self):
        self.render_file_and_optional_save("s0.grb", True, scale=100)

    def test_parser_file_1(self):
        self.render_file_and_optional_save("s1.grb", True, scale=100)

    def test_parser_file_2(self):
        self.render_file_and_optional_save("s2.grb", True, scale=100)

    def test_parser_file_3(self):
        self.render_file_and_optional_save("s3.grb", True, scale=100)

    def test_parser_file_4(self):
        if os.environ.get("PYRELEASE") == "true":
            self.render_file_and_optional_save("s4.grb", True, scale=100)

    def test_parser_file_5(self):
        self.render_file_and_optional_save("s5.grb", True, scale=100)

    def test_parser_file_6(self):
        self.render_file_and_optional_save("s6.grb", True, scale=100)

    def test_parser_file_7(self):
        if os.environ.get("PYRELEASE") == "true":
            self.render_file_and_optional_save("s7.grb", True, scale=100)


if __name__ == "__main__":
    main()
