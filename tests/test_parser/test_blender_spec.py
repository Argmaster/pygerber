# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from pygerber.parser.blender.api import BlenderProjectSpec

TESTS_FOLDER = Path(__file__).parent.parent
RENDERED_PATH = TESTS_FOLDER / Path("gerber/rendered")
GERBER_PATH = TESTS_FOLDER / Path("gerber")


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


if __name__ == "__main__":
    main()
