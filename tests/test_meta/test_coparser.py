# -*- coding: utf-8 -*-
from pygerber.exceptions import FeatureNotSupportedError
from pygerber import meta
from unittest import TestCase, main
from pygerber.meta import coparser

from pygerber.meta.coparser import CoParser
from pygerber.tokens.fs import FormatSpecifierToken


class CoParserTest(TestCase):
    def test_set_default_format(self):
        coparser = CoParser()  # default set in __init__
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

    def test_manual_format_change(self):
        coparser = CoParser()
        coparser.set_mode("I")
        coparser.set_zeros("D")
        self.assertEqual(coparser.format.mode, "I")
        self.assertEqual(coparser.format.zeros, "D")

    def test_parse_coordinates_unsigned_L_short(self):
        coparser = CoParser()
        self.assertEqual(coparser.parse("-300"), -0.0003)
        self.assertEqual(coparser.parse("+300"), 0.0003)
        self.assertEqual(coparser.parse("300"), 0.0003)

    def test_parse_coordinates_L_long(self):
        coparser = CoParser()
        self.assertEqual(coparser.parse("10000300"), 10.0003)
        self.assertEqual(coparser.parse("+10000300"), 10.0003)
        self.assertEqual(coparser.parse("-10000300"), -10.0003)
        self.assertEqual(coparser.dump(-10.0003), "-10000300")
        self.assertEqual(coparser.dump(0.0003), "300")

    def test_parser_coordinates_D(self):
        coparser = CoParser() # 3.6
        coparser.set_zeros("D")
        self.assertEqual(coparser.parse("010000300"), 10.0003)
        self.assertEqual(coparser.parse("-000000300"), -0.0003)

    def test_parser_coordinates_T(self):
        coparser = CoParser() # 3.6
        coparser.set_zeros("T")
        self.assertEqual(coparser.parse("0100003"), 10.0003)
        self.assertEqual(coparser.parse("-0000003"), -0.0003)


    def test_dump_negative(self):
        coparser = CoParser()

    def test_dump_positive(self):
        coparser = CoParser()

    def test_dump_not_supported(self):
        coparser = CoParser()
        coparser.set_zeros("D")
        self.assertRaises(FeatureNotSupportedError, coparser.dump, 0.1)




if __name__ == "__main__":
    main()
