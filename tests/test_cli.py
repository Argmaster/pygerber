# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from pygerber.cli import handle_pygerber_cli

TEMP_FOLDER = Path("tests/.temp")
TEMP_FOLDER.mkdir(0o777, True, True)
save_path = TEMP_FOLDER / "render.png"


class TestCLI(TestCase):
    def test_render_pillow_toml(self):
        handle_pygerber_cli(
            [
                "--pillow",
                "--toml",
                "tests/gerber/pillow/specfile.toml",
                "-s",
                "render.png",
            ]
        )

    def test_render_pillow_yaml(self):
        handle_pygerber_cli(
            [
                "--pillow",
                "--yaml",
                "tests/gerber/pillow/specfile.yaml",
                "-s",
                "render.png",
            ]
        )

    def test_render_pillow_json(self):
        handle_pygerber_cli(
            [
                "--pillow",
                "--json",
                "tests/gerber/pillow/specfile.json",
                "-s",
                "render.png",
            ]
        )

    def test_render_blender_toml(self):
        handle_pygerber_cli(
            [
                "--blender",
                "--toml",
                "tests/gerber/blender/specfile.toml",
                "-s",
                "render.png",
                "--dry",
            ]
        )

    def test_render_blender_yaml(self):
        handle_pygerber_cli(
            [
                "--blender",
                "--yaml",
                "tests/gerber/blender/specfile.yaml",
                "-s",
                "render.png",
                "--dry",
            ]
        )

    def test_render_blender_json(self):
        handle_pygerber_cli(
            [
                "--blender",
                "--json",
                "tests/gerber/blender/specfile.json",
                "-s",
                "render.png",
                "--dry",
            ]
        )


if __name__ == "__main__":
    main()
