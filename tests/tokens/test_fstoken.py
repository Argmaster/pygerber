import re
from unittest import TestCase, main

from pygerber.exceptions import InvalidCommandFormat
from pygerber.meta import Meta
from pygerber.tokens import FormatSpecifierToken



class FormatSpecifierTokenTest(TestCase):
    def test_simple_valid_match(self):
        META = Meta()
        SOURCE = """%FSLAX36Y36*%"""
        fs_token = FormatSpecifierToken.match(SOURCE, 0)
        self.assertTrue(fs_token)
        fs_token.dispatch(META)
        self.assertEqual(fs_token.zeros, "L")
        self.assertEqual(fs_token.mode, "A")
        self.assertEqual(fs_token.X_int, 3)
        self.assertEqual(fs_token.X_dec, 6)
        self.assertEqual(fs_token.Y_int, 3)
        self.assertEqual(fs_token.Y_dec, 6)

    def test_simple_invalid_match(self):
        SOURCE = """%FSLAXx6Y36*%"""
        fs_token = FormatSpecifierToken.match(SOURCE, 0)
        self.assertFalse(fs_token)

    def test_forced_invalid_syntax(self):
        SOURCE = """%FSLAXn6Y36*%"""
        self.setUp_forced_invalid_syntax()
        token = FormatSpecifierToken.match(SOURCE, 0)
        self.assertRaises(
            InvalidCommandFormat, token.dispatch, None
        )
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
        SOURCE = """%FSLAX36Y36*%"""
        fs_token = FormatSpecifierToken.match(SOURCE, 0)
        fs_token.dispatch(META)
        fs_token.affect_meta()
        self.assertEqual(META.coparser.format, fs_token)


if __name__ == "__main__":
    main()
