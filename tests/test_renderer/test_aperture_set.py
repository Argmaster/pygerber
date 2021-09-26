# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest import main

from tests.testutils.apertures import CircleApertureCollector
from tests.testutils.apertures import PolygonApertureCollector
from tests.testutils.apertures import RectangleApertureCollector
from tests.testutils.apertures import RegionApertureCollector
from tests.testutils.apertures import get_dummy_apertureSet


class ApertureSetTest(TestCase):
    def test_getApertureClass(self):
        AS = get_dummy_apertureSet()
        self.assertEqual(AS.getApertureClass("C"), CircleApertureCollector)
        self.assertEqual(AS.getApertureClass("R"), RectangleApertureCollector)
        self.assertEqual(AS.getApertureClass("O"), RectangleApertureCollector)
        self.assertEqual(AS.getApertureClass("P"), PolygonApertureCollector)
        self.assertEqual(AS.getApertureClass(is_region=True), RegionApertureCollector)


if __name__ == "__main__":
    main()
