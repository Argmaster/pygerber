# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PIL import Image
from pygerber.parser.pillow.api import (
    ProjectSpec,
    render_file,
    render_file_and_save,
    render_from_json,
    render_from_spec,
    render_from_toml,
    render_from_yaml,
)
from pygerber.parser.pillow.parser import ImageSizeNullError, ParserWithPillow
from tests.testutils.pillow import are_images_similar

TESTS_FOLDER = Path(__file__).parent.parent
RENDERED_PATH = TESTS_FOLDER / Path("gerber/rendered")
GERBER_PATH = TESTS_FOLDER / Path("gerber")


class TestPillowParser(TestCase):

    SOURCE_0 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            M02*
            """

    def test_parser_string(self):
        parser = ParserWithPillow()
        parser.parse(self.SOURCE_0)
        image = parser.get_image()
        # to manually validate output uncomment this:
        # image.show()
        # to create new comparison image uncomment this:
        # image.save(RENDERED_PATH/"SOURCE_0.png")
        # self.assertTrue(
        #     are_images_similar(Image.open(RENDERED_PATH / "SOURCE_0.png"), image, 0, 0)
        # )

    def test_parser_double_render(self):
        parser = ParserWithPillow()
        self.assertRaises(RuntimeError, lambda: parser.get_image())
        parser.parse(self.SOURCE_0)
        self.assertRaises(RuntimeError, lambda: parser.parse(self.SOURCE_0))
        parser.save(TESTS_FOLDER / "test_parser/test_render.png", "png")
        parser.save(TESTS_FOLDER / "test_parser/test_render.png")

    def test_parser_null_size_image(self):
        parser = ParserWithPillow()
        self.assertRaises(ImageSizeNullError, parser.parse, "M02*")

    def test_render_file_and_save(self):
        render_file_and_save(GERBER_PATH / "s0.grb", RENDERED_PATH / "s0_0.png")

    def render_file_optional_show_and_save(
        self,
        filename: str,
        fulltest: bool = False,
        show: bool = False,
        save: bool = False,
        **kwargs
    ):
        image = render_file(GERBER_PATH / filename, **kwargs)
        if show:
            image.show()
        if save:
            image.save(RENDERED_PATH / (filename.split(".")[0] + ".png"))
        if fulltest:
            self.assertTrue(
                are_images_similar(Image.open(RENDERED_PATH / filename), image, 0, 0)
            )

    def test_parser_file_0(self):
        self.render_file_optional_show_and_save("s0.grb", False, False, False, dpi=1600)

    def test_parser_file_1(self):
        self.render_file_optional_show_and_save("s1.grb", False, False, False, dpi=1600)

    def test_parser_file_2(self):
        self.render_file_optional_show_and_save("s2.grb", False, False, False, dpi=1600)

    def test_parser_file_3(self):
        self.render_file_optional_show_and_save("s3.grb", False, False, False, dpi=1600)

    def test_parser_file_4(self):
        self.render_file_optional_show_and_save("s4.grb", False, False, False, dpi=1600)

    def test_parser_file_5(self):
        self.render_file_optional_show_and_save("s5.grb", False, False, False, dpi=1600)

    def test_parser_file_6(self):
        self.render_file_optional_show_and_save("s6.grb", False, False, False, dpi=1600)

    def test_parser_file_7(self):
        self.render_file_optional_show_and_save("s7.grb", False, False, False, dpi=1600)


def get_test_spec():
    return {
        "dpi": 600,
        "image_padding": 0,
        "ignore_deprecated": True,
        "layers": [
            {
                "file_path": "./tests/gerber/set/top_copper.grb",
                "colors": {
                    "dark": [40, 143, 40, 255],
                    "clear": [60, 181, 60, 255],
                },
            },
            {
                "file_path": "./tests/gerber/set/top_solder_mask.grb",
                "colors": "solder_mask",
            },
            {"file_path": "./tests/gerber/set/top_paste_mask.grb"},
            {
                "file_path": "./tests/gerber/set/top_silk.grb",
                "colors": "silk",
            },
        ],
    }


class ProjectSpecTest(TestCase):
    def test_load_empty(self):
        self.assertRaises(
            TypeError,
            lambda: ProjectSpec(
                {
                    "layers": [
                        {
                            "file_path": "./tests/gerber/set/top_copper.grb",
                            "colors": 444,
                        },
                    ],
                }
            ),
        )

    def test_invalid_color_spec(self):
        self.assertRaises(
            ValueError,
            lambda: ProjectSpec(
                {
                    "layers": [],
                }
            ),
        )

    def test_load(self):
        image = ProjectSpec(get_test_spec()).render()
        # image.show()

    def test_from_json(self):
        image = ProjectSpec.from_json(GERBER_PATH / "pillow" / "specfile.json").render()
        # image.show()

    def test_from_yaml(self):
        image = ProjectSpec.from_yaml(GERBER_PATH / "pillow" / "specfile.yaml").render()
        # image.show()

    def test_from_toml(self):
        image = ProjectSpec.from_toml(GERBER_PATH / "pillow" / "specfile.toml").render()
        # image.show()


class TestAPI(TestCase):
    def test_render_from_spec(self):
        image = render_from_spec(get_test_spec())
        # image.show()

    def test_render_from_json(self):
        image = render_from_json(GERBER_PATH / "pillow" / "specfile.json")
        # image.show()

    def test_render_from_yaml(self):
        image = render_from_yaml(GERBER_PATH / "pillow" / "specfile.yaml")
        # image.show()

    def test_render_from_toml(self):
        image = render_from_toml(GERBER_PATH / "pillow" / "specfile.toml")
        # image.show()


if __name__ == "__main__":
    main()
