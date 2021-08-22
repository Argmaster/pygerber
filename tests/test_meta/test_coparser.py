# -*- coding: utf-8 -*-
from pygerber import meta
from unittest import TestCase, main

from pygerber.meta.coparser import CoParser
from pygerber.tokens.fs import FormatSpecifierToken


class CoParserTest(TestCase):
    def test_set_default_format(self):
        coparser = CoParser() # default set in __init__
        self.assertEqual(coparser.format.length, 9)
        self.assertEqual(coparser.format.INT_FORMAT, 3)
        self.assertEqual(coparser.format.DEC_FORMAT, 6)

    def test_set_format(self):
        fs = FormatSpecifierToken.match_and_dispatch(None, r"%FSLAX25Y25*%")
        coparser = CoParser()
        coparser.set_format(fs)
        self.assertEqual(coparser.format.length, 7)
        self.assertEqual(coparser.format.INT_FORMAT, 2)
        self.assertEqual(coparser.format.DEC_FORMAT, 5)

    def test_parse_coordinates_unsigned_short(self):
        coparser = CoParser()
        self.assertEqual(coparser.parse("300"), 0.0003)

    def test_parse_coordinates_positive_short(self):
        coparser = CoParser()
        self.assertEqual(coparser.parse("+300"), 0.0003)

    def test_parse_coordinates_negative_short(self):
        coparser = CoParser()
        self.assertEqual(coparser.parse("-300"), -0.0003)

    def test_parse_coordinates_unsigned_long(self):
        coparser = CoParser()
        self.assertEqual(coparser.parse("10000300"), 10.0003)

    def test_parse_coordinates_positive_long(self):
        coparser = CoParser()
        self.assertEqual(coparser.parse("+10000300"), 10.0003)

    def test_parse_coordinates_negative_long(self):
        coparser = CoParser()
        self.assertEqual(coparser.parse("-10000300"), -10.0003)


if __name__ == "__main__":
    main()