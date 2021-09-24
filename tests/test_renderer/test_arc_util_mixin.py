# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from pygerber.renderer.arc_util_mixin import ArcUtilMixin


class ArcUtilMixinTest(TestCase):
    def test_get_arc_traverse_step_angle(self):
        self.assertRaises(
            NotImplementedError,
            lambda: ArcUtilMixin.get_arc_traverse_step_angle(None, None, None, None),
        )


if __name__ == "__main__":
    main()
