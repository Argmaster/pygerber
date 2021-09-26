# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase
from unittest import main

from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin


class Test(TestCase):
    def test_draw_shape(self):
        self.assertRaises(
            NotImplementedError, lambda: FlashUtilMixin.draw_shape(None, None, None)
        )


if __name__ == "__main__":
    main()
