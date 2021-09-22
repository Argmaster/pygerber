# -*- coding: utf-8 -*-
from unittest.mock import Mock
from pygerber.drawing_state import DrawingState
from unittest import TestCase, main

from pygerber.tokens import D02_Token


class D02_TokenText(TestCase):
    def parse_token(self, source):
        re_match = D02_Token.regex.match(source, 0)
        if re_match is not None:
            return D02_Token(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")

    def assertValues(self, token, X, Y):
        self.assertTrue(
            token.X == X and token.Y == Y, f"{token.X} == {X} and {token.Y} == {Y}"
        )

    def test_valid_match(self):
        token = self.parse_token("X1700Y2000D02*")
        self.assertValues(token, 0.0017, 0.002)

    def test_one_arg_missing(self):
        token = self.parse_token("X-600000D02*")
        self.assertValues(token, -0.6, None)

    def test_invalid_match(self):
        self.assertRaises(RuntimeError, lambda: self.parse_token("X1700Y2000D01*"))

    def get_renderer_mock(self):
        return Mock(
            move_pointer=Mock(),
        )

    def test_post_render(self):
        token = self.parse_token("X600000D02*")
        renderer = self.get_renderer_mock()
        token.post_render(renderer)
        renderer.move_pointer.assert_called_with(token.point)

if __name__ == "__main__":
    main()