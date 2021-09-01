# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.parser.pillow.apertures.flash_mixin import FlashUtilMixin
from unittest import TestCase, main


class Test(TestCase):
    def test_draw_shape(self):
        self.assertRaises(
            NotImplementedError, lambda: FlashUtilMixin.draw_shape(None, None, None)
        )


if __name__ == "__main__":
    main()
