# -*- coding: utf-8 -*-
from unittest import TestCase, main

from pygerber.drawing_state import DrawingState
from pygerber.tokens import FormatSpecifierToken


class FormatSpecifierTokenTest(TestCase):
    def match_fs_token(self, SOURCE) -> FormatSpecifierToken:
        re_match = FormatSpecifierToken.regex.match(SOURCE)
        if re_match is not None:
            return FormatSpecifierToken(re_match, self)
        else:
            raise RuntimeError(f"Token not matched for {SOURCE}")

    def test_simple_valid_match(self):
        fs_token = self.match_fs_token("""%FSLAX36Y36*%""")
        self.assertEqual(fs_token.zeros, "L")
        self.assertEqual(fs_token.mode, "A")
        self.assertEqual(fs_token.X_int, 3)
        self.assertEqual(fs_token.X_dec, 6)
        self.assertEqual(fs_token.Y_int, 3)
        self.assertEqual(fs_token.Y_dec, 6)

    def test_properties(self):
        fs_token = self.match_fs_token("""%FSLAX36Y36*%""")
        self.assertEqual(fs_token.length, 9)
        self.assertEqual(fs_token.INT_FORMAT, 3)
        self.assertEqual(fs_token.DEC_FORMAT, 6)

    def test_simple_invalid_match(self):
        SOURCE = r"%FSLAXx6Y36*%"
        fs_token = FormatSpecifierToken.regex.match(SOURCE)
        self.assertTrue(fs_token is None)

    def test_alter_state(self):
        fs_token = self.match_fs_token("""%FSLAX36Y36*%""")
        state = DrawingState()
        fs_token.alter_state(state)
        self.assertEqual(state.coparser.format, fs_token)

    def test_deprecated_unequal_int_specifiers(self):
        SOURCE = r"%FSLIX36Y26*%"
        fs_token = self.match_fs_token(SOURCE)
        self.assertTrue(fs_token.__deprecated__ is not None)

    def test_deprecated_unequal_dec_specifiers(self):
        SOURCE = r"%FSLIX36Y35*%"
        fs_token = self.match_fs_token(SOURCE)
        self.assertTrue(fs_token.__deprecated__ is not None)

    def test_stringify(self):
        fs_token = self.match_fs_token(r"""%FSLAX36Y36*%""")
        self.assertEqual(str(fs_token), r"%FSLAX36Y36*%")


if __name__ == "__main__":
    main()
