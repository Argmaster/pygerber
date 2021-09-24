# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from unittest import TestCase, main


class TestCLI(TestCase):
    def test_render_pillow_single_file(self):
        save_path = "render.png"
        if os.path.exists(save_path):
            os.remove(save_path)
        os.system(
            f'python -m pygerber --pillow --file "tests\\gerber\\s5.grb" -s "{save_path}"'
        )
        self.assertTrue(os.path.exists(save_path))

    def test_render_pillow_multi_file(self):
        save_path = "render.png"
        if os.path.exists(save_path):
            os.remove(save_path)
        os.system(
            f'python -m pygerber --pillow --toml "tests\\gerber\\pillow\\specfile.toml" -s "{save_path}"'
        )
        self.assertTrue(os.path.exists(save_path))


if __name__ == "__main__":
    main()
