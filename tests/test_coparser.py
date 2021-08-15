from unittest import TestCase, main

from pygerber.coparser import CoParser


class CoParserTest(TestCase):
    def test_set_default_format(self):
        coparser = CoParser()
        coparser.set_default_format()
        self.assertEqual(coparser.format.length, 9)
        self.assertEqual(coparser.format.INT_FORMAT, 3)
        self.assertEqual(coparser.format.DEC_FORMAT, 6)

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