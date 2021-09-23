from unittest import TestCase, main

from pygerber.tokens import G04_Token, G74_Token, G75_Token
from pygerber.exceptions import DeprecatedSyntax


class TestCommentTokens(TestCase):
    def test_G04(self):
        source = "G04 This is a comment*"
        token = G04_Token.regex.match(source, 0)
        self.assertTrue(token)
        self.assertEqual(token.STRING, " This is a comment")

    def test_G75(self):
        source = "G75*"
        token = G75_Token.match(source)
        self.assertTrue(token)

    def test_G74(self):
        source = "G74*"
        token = G74_Token.regex.match(source)
        self.assertTrue(token)

    def test_G74_deprecated_fail(self):
        source = "G74*"
        token = G74_Token.regex.match(source)
        self.assertTrue(token)


if __name__ == "__main__":
    main()
