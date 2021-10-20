# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from unittest import TestCase, main


class TestCLI(TestCase):
    def test_render_pillow_multi_file(self):
        save_path = "render.png"
        try:
            os.remove(save_path)
        except Exception:
            pass
        value = os.system(
            f'python -m pygerber --pillow --toml "tests/gerber/pillow/specfile.toml" -s "{save_path}"'
        )
        self.assertEqual(value, 0)

    def test_render_blender_multi_file(self):
        save_path = "render.png"
        try:
            os.remove(save_path)
        except Exception:
            pass
        value = os.system(
            f'python -m pygerber --blender --toml "tests/gerber/blender/specfile.toml" -s "{save_path}" --dry'
        )
        self.assertEqual(value, 0)


if __name__ == "__main__":
    main()
