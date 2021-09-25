# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from pygerber.exceptions import InvalidSyntaxError, TokenNotFound
from pygerber.tokenizer import Tokenizer

from pathlib import Path

TESTS_FOLDER = Path(__file__).parent


class TokenizerTest(TestCase):

    SOURCE_0 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            M02*
            """

    SOURCE_1 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            """

    SOURCE_2 = """
        XDD
    """

    def test_tokenize_string(self):
        tokenizer = Tokenizer()
        tokenizer.tokenize(self.SOURCE_0)
        self.assertEqual(tokenizer.token_stack_size, 6)

    def test_tokenize_string_no_end(self):
        tokenizer = Tokenizer()
        self.assertRaises(InvalidSyntaxError, lambda: tokenizer.tokenize(self.SOURCE_1))

    def test_tokenize_file_invalid_syntax(self):
        tokenizer = Tokenizer()
        path = TESTS_FOLDER / "gerber\\invalid_syntax.grb"
        with open(path) as file:
            self.assertRaises(
                InvalidSyntaxError, lambda: tokenizer.tokenize(file.read(), path)
            )

    def test_tokenize_string_token_not_found(self):
        tokenizer = Tokenizer()
        self.assertRaises(TokenNotFound, lambda: tokenizer.tokenize(self.SOURCE_2))

    def test_tokenize_file_0(self):
        tokenizer = Tokenizer()
        tokenizer.tokenize_file(TESTS_FOLDER / "gerber/s0.grb")
        self.assertEqual(tokenizer.token_stack_size, 17)

    def test_tokenize_file_1(self):
        tokenizer = Tokenizer()
        tokenizer.tokenize_file(TESTS_FOLDER / "gerber/s1.grb")
        self.assertEqual(tokenizer.token_stack_size, 47)

    def test_tokenize_file_2(self):
        tokenizer = Tokenizer()
        tokenizer.tokenize_file(TESTS_FOLDER / "gerber/s2.grb")
        self.assertEqual(tokenizer.token_stack_size, 116)


if __name__ == "__main__":
    main()
