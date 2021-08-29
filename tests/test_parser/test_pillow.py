# -*- coding: utf-8 -*-
from __future__ import annotations

import unittest
from unittest import TestCase, main

from pygerber.parser.pillow.parser import ParserWithPillow


class TestPillowParser(TestCase):

    SOURCE_0 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            M02*
            """

    def test_parser_string(self):
        parser = ParserWithPillow(None, self.SOURCE_0)
        self.assertEqual(parser.tokenizer.bbox.width(), 1.5)
        parser.render()
        image = parser.get_image()
        # should display circle
        # image.show()

    def test_parser_file_0(self):
        parser = ParserWithPillow("./tests/gerber/s3.grb", dpi=1600)
        parser.render()
        image = parser.get_image()
        # image.show()

    def test_parser_file_1(self):
        parser = ParserWithPillow("./tests/gerber/s4.grb")
        parser.render()
        image = parser.get_image()
        image.show()

    def test_parser_file_2(self):
        parser = ParserWithPillow("./tests/gerber/s5.grb")
        parser.render()
        image = parser.get_image()
        image.show()


if __name__ == "__main__":
    main()
