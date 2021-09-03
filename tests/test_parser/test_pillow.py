# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from tests.testutils.pillow import are_images_similar
from unittest import TestCase, main

from PIL import Image
from pygerber.parser.pillow.parser import (
    ColorSet,
    ImageSizeNullError,
    LayerSpec,
    ParserWithPillow,
)

RENDERED_PATH = Path("./tests/gerber/rendered")
GERBER_PATH = Path("./tests/gerber")


class TestPillowParser(TestCase):

    SOURCE_0 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            M02*
            """

    def test_parser_double_none(self):
        self.assertRaises(RuntimeError, lambda: ParserWithPillow(None, None))

    def test_parser_string(self):
        parser = ParserWithPillow(None, self.SOURCE_0)
        self.assertEqual(parser.tokenizer.bbox.width(), 1.5)
        parser.render()
        image = parser.get_image()
        # to manually validate output uncomment this:
        # image.show()
        # to create new comparison image uncomment this:
        # image.save(RENDERED_PATH/"SOURCE_0.png")
        # self.assertTrue(
        #     are_images_similar(Image.open(RENDERED_PATH / "SOURCE_0.png"), image, 0, 0)
        # )

    def test_parser_double_render(self):
        parser = ParserWithPillow(None, self.SOURCE_0)
        self.assertRaises(RuntimeError, lambda: parser.get_image())
        parser.render()
        self.assertRaises(RuntimeError, lambda: parser.render())
        parser.save(".\\tests\\test_parser\\test_render.png", "png")
        parser.save(".\\tests\\test_parser\\test_render.png")

    def test_parser_null_size_image(self):
        parser = ParserWithPillow(None, "M02*")
        self.assertRaises(ImageSizeNullError, parser.render)

    def test_render_file_and_save(self):
        ParserWithPillow.render_file_and_save(
            GERBER_PATH / "s0.grb", RENDERED_PATH / "s0_0.png"
        )

    def render_file_optional_show_and_save(
        self,
        filename: str,
        fulltest: bool = False,
        show: bool = False,
        save: bool = False,
        **kwargs
    ):
        image = ParserWithPillow.render_file(GERBER_PATH / filename, **kwargs)
        if show:
            image.show()
        if save:
            image.save(RENDERED_PATH / (filename.split(".")[0] + ".png"))
        if fulltest:
            self.assertTrue(
                are_images_similar(Image.open(RENDERED_PATH / filename), image, 0, 0)
            )

    def test_parser_file_0(self):
        self.render_file_optional_show_and_save("s0.grb", False, False, True, dpi=1600)

    def test_parser_file_1(self):
        self.render_file_optional_show_and_save("s1.grb", False, False, True, dpi=1600)

    def test_parser_file_2(self):
        self.render_file_optional_show_and_save("s2.grb", False, False, True, dpi=1600)

    def test_parser_file_3(self):
        self.render_file_optional_show_and_save("s3.grb", False, False, True, dpi=1600)

    def test_parser_file_4(self):
        self.render_file_optional_show_and_save("s4.grb", False, False, True, dpi=1600)

    def test_parser_file_5(self):
        self.render_file_optional_show_and_save("s5.grb", False, False, True, dpi=1600)

    def test_parser_file_6(self):
        self.render_file_optional_show_and_save("s6.grb", False, False, True, dpi=1600)

    def test_parser_file_7(self):
        self.render_file_optional_show_and_save("s7.grb", False, False, True, dpi=1600)

    def test_render_multilayer(self):
        images = ParserWithPillow.render_all(
            [
                LayerSpec(
                    GERBER_PATH / "set" / "top_copper.grb",
                    ColorSet((50, 168, 82, 255), (71, 196, 105, 255)),
                ),
                LayerSpec(
                    GERBER_PATH / "set" / "top_silk.grb", ColorSet((255, 255, 255, 255))
                ),
                LayerSpec(
                    GERBER_PATH / "set" / "top_paste_mask.grb",
                    ColorSet((117, 117, 117, 255)),
                ),
                LayerSpec(
                    GERBER_PATH / "set" / "top_solder_mask.grb",
                    ColorSet((153, 153, 153, 255)),
                ),
            ]
        )
        for image in images:
            image.show()


if __name__ == "__main__":
    main()
