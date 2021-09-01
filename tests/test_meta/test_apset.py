# -*- coding: utf-8 -*-
from tests.testutils.apertures import CircleApertureCollector, PolygonApertureCollector, RectangleApertureCollector, RegionApertureCollector, get_dummy_apertureSet
from unittest import TestCase, main

class ApertureSetTest(TestCase):

    def test_getApertureClass(self):
        AS = get_dummy_apertureSet()
        self.assertEqual(AS.getApertureClass("C"), CircleApertureCollector)
        self.assertEqual(AS.getApertureClass("R"), RectangleApertureCollector)
        self.assertEqual(AS.getApertureClass("O"), RectangleApertureCollector)
        self.assertEqual(AS.getApertureClass("P"), PolygonApertureCollector)
        self.assertEqual(AS.getApertureClass(is_region=True), RegionApertureCollector)



if __name__ == '__main__':
    main()