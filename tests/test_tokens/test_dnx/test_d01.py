# -*- coding: utf-8 -*-
from unittest.mock import Mock
from pygerber.renderer import Renderer
from pygerber.mathclasses import Vector2D
from pygerber.drawing_state import DrawingState
from unittest import TestCase, main

from pygerber.tokens import D01_Token


class D01_TokenTest(TestCase):
    def parse_token(self, source):
        re_match = D01_Token.regex.match(source, 0)
        if re_match is not None:
            return D01_Token(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")

    def assertValues(self, token, X, Y, I, J):
        self.assertTrue(
            token.X == X and token.Y == Y and token.I == I and token.J == J,
            f"{token.X} == {X} and {token.Y} == {Y} and {token.I} == {I} and {token.J} == {J}",
        )

    def test_valid_match_ij(self):
        token = self.parse_token("I300J100D01*")
        self.assertValues(token, None, None, 0.0003, 0.0001)

    def test_valid_match_xy(self):
        token = self.parse_token("X1700Y2000D01*")
        self.assertValues(token, 0.0017, 0.002, None, None)

    def test_valid_match_y(self):
        token = self.parse_token("Y500000D01*")
        self.assertValues(token, None, 0.5, None, None)

    def test_valid_match_signed(self):
        token = self.parse_token("X-300Y+200I50J50D01*")
        self.assertValues(token, -0.0003, 0.0002, 0.00005, 0.00005)

    def test_no_match(self):
        SOURCE = "H333I300J100D01*"
        token = D01_Token.regex.match(SOURCE)
        self.assertTrue(token is None)

    def test_end(self):
        token = self.parse_token("X-300Y+200I50J50D01*")
        self.assertEqual(Vector2D(-0.0003, 0.0002), token.end)

    def test_offset(self):
        token = self.parse_token("X-300Y+200I50J50D01*")
        self.assertEqual(Vector2D(0.00005, 0.00005), token.offset)

    def get_renderer_mock(self):
        return Mock(
            draw_interpolated=Mock(),
            move_pointer=Mock(),
            bbox_interpolated=Mock(),
        )

    def test_render(self):
        token = self.parse_token("X-300Y+200I50J50D01*")
        renderer = self.get_renderer_mock()
        token.render(renderer)
        renderer.draw_interpolated.assert_called_with(token.end, token.offset)

    def test_post_render(self):
        token = self.parse_token("X-300Y+200I50J50D01*")
        renderer = self.get_renderer_mock()
        token.post_render(renderer)
        renderer.move_pointer.assert_called_with(token.end)

    def test_bbox(self):
        token = self.parse_token("X-300Y+200I50J50D01*")
        renderer = self.get_renderer_mock()
        token.bbox(renderer)
        renderer.bbox_interpolated.assert_called_with(token.end, token.offset)


if __name__ == "__main__":
    main()
