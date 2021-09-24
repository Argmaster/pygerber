# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from pygerber.tokens.control import (
    EndOfStream_Token,
    ImagePolarity_Token,
    Whitespace_Token,
)


class TestControlTokens(TestCase):
    def test_EndOfStream_Token(self):
        self.assertIsNotNone(EndOfStream_Token.regex.match("M02*"))

    def test_WhitespaceToken(self):
        self.assertTrue(len(Whitespace_Token.regex.match("     \n\t ").group()) == 8)

    def test_ImagePolarity_Token(self):
        self.assertIsNotNone(ImagePolarity_Token.__deprecated__)
        self.asserstIsNotNone(ImagePolarity_Token.regex.match("%IPPOS*%"))
        self.assertIsNotNone(ImagePolarity_Token.regex.match("%IPNEG*%"))


if __name__ == "__main__":
    main()
