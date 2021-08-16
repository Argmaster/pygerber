import re
from unittest import TestCase, main

from pygerber.exceptions import DeprecatedSyntax, InvalidCommandFormat
from pygerber.meta import Meta
from pygerber.tokens import FormatSpecifierToken


class FormatSpecifierTokenTest(TestCase):

    def parse_and_dispatch(self, META, SOURCE, BEIGN) -> FormatSpecifierToken:
        fs_token = FormatSpecifierToken.match(SOURCE, BEIGN)
        self.assertTrue(fs_token)
        fs_token.dispatch(META)
        return fs_token

    def test_simple_valid_match(self):
        fs_token = self.parse_and_dispatch(Meta(), """%FSLAX36Y36*%""", 0)
        self.assertEqual(fs_token.zeros, "L")
        self.assertEqual(fs_token.mode, "A")
        self.assertEqual(fs_token.X_int, 3)
        self.assertEqual(fs_token.X_dec, 6)
        self.assertEqual(fs_token.Y_int, 3)
        self.assertEqual(fs_token.Y_dec, 6)

    def test_cached_properties(self):
        fs_token = self.parse_and_dispatch(Meta(), """%FSLAX36Y36*%""", 0)
        self.assertEqual(fs_token.length, 9)
        self.assertEqual(fs_token.INT_FORMAT, 3)
        self.assertEqual(fs_token.DEC_FORMAT, 6)

    def test_simple_invalid_match(self):
        SOURCE = """%FSLAXx6Y36*%"""
        fs_token = FormatSpecifierToken.match(SOURCE, 0)
        self.assertFalse(fs_token)

    def test_forced_invalid_syntax(self):
        SOURCE = """%FSLAXn6Y36*%"""
        self.setUp_forced_invalid_syntax()
        token = FormatSpecifierToken.match(SOURCE, 0)
        self.assertRaises(InvalidCommandFormat, token.dispatch, None)
        self.cleanUp_forced_invalid_syntax()

    def setUp_forced_invalid_syntax(self):
        self.ORIGINAL_REGEX = FormatSpecifierToken.regex
        FormatSpecifierToken.regex = re.compile(  # forcibly changed regex to accept damaged pattern
            r"%FS(?P<zeros>[LTD])(?P<mode>[AI])X(?P<X_int>[1-6n])(?P<X_dec>[1-6])Y(?P<Y_int>[1-6])(?P<Y_dec>[1-6])\*%"
        )

    def cleanUp_forced_invalid_syntax(self):
        FormatSpecifierToken.regex = self.ORIGINAL_REGEX

    def test_affect_meta(self):
        META = Meta()
        fs_token = self.parse_and_dispatch(META, """%FSLAX36Y36*%""", 0)
        fs_token.affect_meta()
        self.assertEqual(META.coparser.format, fs_token)

    def test_deprecated_inequal_int_specifiers(self):
        META = Meta(ignore_deprecated=False)
        SOURCE = """%FSLIX36Y26*%"""
        fs_token = FormatSpecifierToken.match(SOURCE, 0)
        self.assertRaises(DeprecatedSyntax, fs_token.dispatch, META)

    def test_deprecated_inequal_dec_specifiers(self):
        META = Meta(ignore_deprecated=False)
        SOURCE = """%FSLIX36Y35*%"""
        fs_token = FormatSpecifierToken.match(SOURCE, 0)
        self.assertRaises(DeprecatedSyntax, fs_token.dispatch, META)

if __name__ == "__main__":
    main()
