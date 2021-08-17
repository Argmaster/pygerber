from unittest import TestCase, main

from pygerber.meta import Meta
from pygerber.tokens import G04Token, G74Token, G75Token
from pygerber.exceptions import DeprecatedSyntax


class TestCommentTokens(TestCase):
    def test_G04(self):
        META = Meta()
        source = "G04 This is a comment*"
        token = G04Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        self.assertEqual(token.STRING, " This is a comment")

    def test_G75(self):
        META = Meta()
        source = "G75*"
        token = G75Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)

    def test_G74(self):
        META = Meta()
        source = "G74*"
        token = G74Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)

    def test_G74_deprecated_fail(self):
        META = Meta(ignore_deprecated=False)
        source = "G74*"
        token = G74Token.match(source, 0)
        self.assertTrue(token)
        self.assertRaises(DeprecatedSyntax, token.dispatch, META)


if __name__ == "__main__":
    main()
