# -*- coding: utf-8 -*-
from __future__ import annotations

from types import SimpleNamespace
from unittest import TestCase, main

from pygerber.exceptions import ApertureSelectionError, InvalidSyntaxError
from tests.testutils.aperture_manager import get_dummy_bound_aperture_manager
from tests.testutils.apertures import CircleApertureCollector, CustomApertureCollector


class ApertureManagerTest(TestCase):
    def test_define_aperture_C(self):
        am = get_dummy_bound_aperture_manager()
        args = SimpleNamespace(
            DIAMETER=0.2,
            HOLE_DIAMETER=0,
        )
        am.define_aperture("C", None, 10, args)
        self.assertEqual(type(am.apertures[10]), CircleApertureCollector)
        self.assertEqual(am.apertures[10].DIAMETER, args.DIAMETER)
        self.assertEqual(am.apertures[10].HOLE_DIAMETER, args.HOLE_DIAMETER)

    def test_define_custom_aperture(self):
        am = get_dummy_bound_aperture_manager()
        args = SimpleNamespace(
            ARG1=1,
            ARG2=2,
        )
        am.define_aperture(None, "THERMAL", 10, args)
        self.assertEqual(type(am.apertures[10]), CustomApertureCollector)

    def test_define_aperture_fail(self):
        am = get_dummy_bound_aperture_manager()
        args = SimpleNamespace(
            DIAMETER=0.2,
            HOLE_DIAMETER=0,
        )
        am.define_aperture("C", None, 10, args)
        self.assertRaises(
            InvalidSyntaxError, lambda: am.define_aperture("C", None, 10, args)
        )

    def test_get_aperture(self):
        am = get_dummy_bound_aperture_manager()
        args = SimpleNamespace(
            DIAMETER=0.2,
            HOLE_DIAMETER=0,
        )
        am.define_aperture("C", None, 10, args)
        self.assertEqual(am.apertures[10], am.get_aperture(10))

    def test_get_aperture_fail(self):
        am = get_dummy_bound_aperture_manager()
        self.assertRaises(ApertureSelectionError, am.get_aperture, 10)


if __name__ == "__main__":
    main()
