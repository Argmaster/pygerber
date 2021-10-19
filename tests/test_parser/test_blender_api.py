# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from pathlib import Path
from unittest import TestCase, main

from PyR3.shortcut.io import export_to

from pygerber.API3D import (
    render_from_json,
    render_from_spec,
    render_from_toml,
    render_from_yaml,
)
from pygerber.parser.blender.api import _skip_next_render

TESTS_FOLDER = Path(__file__).parent.parent
RENDERED_PATH = TESTS_FOLDER / Path("gerber/rendered")
GERBER_PATH = TESTS_FOLDER / Path("gerber")


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


class TestAPI(TestCase):
    def test_render_from_spec(self):
        if os.environ.get("PYRELEASE") != "true":
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
