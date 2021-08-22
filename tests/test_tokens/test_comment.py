from unittest import TestCase, main

from pygerber.meta import Meta
from pygerber.tokens import G04_Token, G74_Token, G75_Token
from pygerber.exceptions import DeprecatedSyntax


class TestCommentTokens(TestCase):
    def test_G04(self):
        META = Meta(None)
        source = "G04 This is a comment*"
        token = G04_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        self.assertEqual(token.STRING, " This is a comment")

    def test_G75(self):
        META = Meta(None)
        source = "G75*"
        token = G75_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)

    def test_G74(self):
        META = Meta(None)
        source = "G74*"
        token = G74_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)

    def test_G74_deprecated_fail(self):
        META = Meta(None, ignore_deprecated=False)
        source = "G74*"
        token = G74_Token.match(source, 0)
        self.assertTrue(token)
        self.assertRaises(DeprecatedSyntax, token.dispatch, META)


if __name__ == "__main__":
    main()
