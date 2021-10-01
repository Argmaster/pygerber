# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase
from unittest import main

# from pygerber.parser.blender.api import ProjectSpec
from pygerber.parser.blender.api import render_file
from pygerber.parser.blender.api import render_file_and_save

# from pygerber.parser.blender.api import render_from_json
# from pygerber.parser.blender.api import render_from_spec
# from pygerber.parser.blender.api import render_from_toml
# from pygerber.parser.blender.api import render_from_yaml
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
        parser.save(RENDERED_PATH / "SOURCE_0.glb")

    def test_parser_double_render(self):
        parser = ParserWithBlender()
        self.assertRaises(RuntimeError, lambda: parser.get_image())
        parser.parse(self.SOURCE_0)
        self.assertRaises(RuntimeError, lambda: parser.parse(self.SOURCE_0))
        parser.save(TESTS_FOLDER / "test_parser/test_render.glb")

    def test_render_file_and_save(self):
        render_file_and_save(GERBER_PATH / "s0.grb", RENDERED_PATH / "s0_0.glb")

    def render_file_optional_show_and_save(
        self, filename: str, show: bool = False, save: bool = False, **kwargs
    ):
        image = render_file(GERBER_PATH / filename, **kwargs)
        if show:
            image.show()
        if save:
            image.save(RENDERED_PATH / (filename.split(".")[0] + ".glb"))

    def test_parser_file_0(self):
        self.render_file_optional_show_and_save("s0.grb", False, False, scale=100)

    def test_parser_file_1(self):
        self.render_file_optional_show_and_save("s1.grb", False, False, scale=100)

    def test_parser_file_2(self):
        self.render_file_optional_show_and_save("s2.grb", False, False, scale=100)

    def test_parser_file_3(self):
        self.render_file_optional_show_and_save("s3.grb", False, False, scale=100)

    def test_parser_file_4(self):
        self.render_file_optional_show_and_save("s4.grb", False, False, scale=100)

    def test_parser_file_5(self):
        self.render_file_optional_show_and_save("s5.grb", False, False, scale=100)

    def test_parser_file_6(self):
        self.render_file_optional_show_and_save("s6.grb", False, False, scale=100)

    def test_parser_file_7(self):
        self.render_file_optional_show_and_save("s7.grb", False, False, scale=100)


# def get_test_spec():
#     return {
#         "dpi": 600,
#         "image_padding": 0,
#         "ignore_deprecated": True,
#         "layers": [
#             {
#                 "file_path": "./tests/gerber/set/top_copper.grb",
#                 "colors": {
#                     "dark": [40, 143, 40, 255],
#                     "clear": [60, 181, 60, 255],
#                 },
#             },
#             {
#                 "file_path": "./tests/gerber/set/top_solder_mask.grb",
#                 "colors": "solder_mask",
#             },
#             {"file_path": "./tests/gerber/set/top_paste_mask.grb"},
#             {
#                 "file_path": "./tests/gerber/set/top_silk.grb",
#                 "colors": "silk",
#             },
#         ],
#     }


# class ProjectSpecTest(TestCase):
#     def test_load_empty(self):
#         self.assertRaises(
#             TypeError,
#             lambda: ProjectSpec(
#                 {
#                     "layers": [
#                         {
#                             "file_path": "./tests/gerber/set/top_copper.grb",
#                             "colors": 444,
#                         },
#                     ],
#                 }
#             ),
#         )
#
#     def test_invalid_color_spec(self):
#         self.assertRaises(
#             ValueError,
#             lambda: ProjectSpec(
#                 {
#                     "layers": [],
#                 }
#             ),
#         )
#
#     def test_load(self):
#         image = ProjectSpec(get_test_spec()).render()
#         # image.show()
#
#     def test_from_json(self):
#         image = ProjectSpec.from_json(GERBER_PATH / "blender" / "specfile.json").render()
#         # image.show()
#
#     def test_from_yaml(self):
#         image = ProjectSpec.from_yaml(GERBER_PATH / "blender" / "specfile.yaml").render()
#         # image.show()
#
#     def test_from_toml(self):
#         image = ProjectSpec.from_toml(GERBER_PATH / "blender" / "specfile.toml").render()
#         # image.show()


# class TestAPI(TestCase):
#     def test_render_from_spec(self):
#         image = render_from_spec(get_test_spec())
#         # image.show()
#
#     def test_render_from_json(self):
#         image = render_from_json(GERBER_PATH / "blender" / "specfile.json")
#         # image.show()
#
#     def test_render_from_yaml(self):
#         image = render_from_yaml(GERBER_PATH / "blender" / "specfile.yaml")
#         # image.show()
#
#     def test_render_from_toml(self):
#         image = render_from_toml(GERBER_PATH / "blender" / "specfile.toml")
#         # image.show()


if __name__ == "__main__":
    main()
