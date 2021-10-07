# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase
from unittest import main

from PyR3.shortcut.io import export_to

from pygerber.API3D import render_file
from pygerber.API3D import render_file_and_save
from pygerber.API3D import render_from_json
from pygerber.API3D import render_from_spec
from pygerber.API3D import render_from_toml
from pygerber.API3D import render_from_yaml
from pygerber.parser.blender.api import BlenderProjectSpec
from pygerber.parser.blender.api import _skip_next_render
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
        pass
        # self.render_file_and_optional_save("s4.grb", True, scale=100)

    def test_parser_file_5(self):
        self.render_file_and_optional_save("s5.grb", True, scale=100)

    def test_parser_file_6(self):
        self.render_file_and_optional_save("s6.grb", True, scale=100)

    def test_parser_file_7(self):
        pass
        # self.render_file_and_optional_save("s7.grb", True, scale=100)


def get_test_spec():
    return {
        "ignore_deprecated": True,
        "layers": [
            {
                "file_path": "./tests/gerber/set/top_copper.grb",
                "structure": {
                    "material": {
                        "color": [40, 143, 40, 255],
                        "metallic": 1.0,
                        "roughness": 0.8,
                    },
                    "thickness": 0.78,
                },
            },
            {
                "file_path": "./tests/gerber/set/top_solder_mask.grb",
                "structure": "solder_mask",
            },
            {"file_path": "./tests/gerber/set/top_paste_mask.grb"},
            {
                "file_path": "./tests/gerber/set/top_silk.grb",
                "structure": "silk",
            },
        ],
    }


class ProjectSpecTest(TestCase):
    def test_load_empty(self):
        self.assertRaises(
            TypeError,
            lambda: BlenderProjectSpec(
                {
                    "layers": [
                        {
                            "file_path": "./tests/gerber/set/top_copper.grb",
                            "structure": 444,
                        },
                    ],
                }
            ),
        )

    def test_invalid_color_spec(self):
        self.assertRaises(
            ValueError,
            lambda: BlenderProjectSpec(
                {
                    "layers": [],
                }
            ),
        )


class TestAPI(TestCase):
    def test_render_from_spec(self):
        _skip_next_render()
        render_from_spec(get_test_spec())
        export_to(RENDERED_PATH / "blender" / "TestAPI_from_spec.glb")

    def test_render_from_json(self):
        _skip_next_render()
        render_from_json(GERBER_PATH / "blender" / "specfile.json")
        export_to(RENDERED_PATH / "blender" / "TestAPI_from_json.glb")

    def test_render_from_yaml(self):
        _skip_next_render()
        render_from_yaml(GERBER_PATH / "blender" / "specfile.yaml")
        export_to(RENDERED_PATH / "blender" / "TestAPI_from_yaml.glb")

    def test_render_from_toml(self):
        _skip_next_render()
        render_from_toml(GERBER_PATH / "blender" / "specfile.toml")
        export_to(RENDERED_PATH / "blender" / "TestAPI_from_toml.glb")


if __name__ == "__main__":
    main()
