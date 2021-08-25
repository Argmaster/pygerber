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

    def test_parser(self):
        #ParserWithPillow()
        pass


if __name__ == "__main__":
    main()
