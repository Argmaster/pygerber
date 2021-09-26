# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest import main
from unittest.mock import Mock

from pygerber.drawing_state import DrawingState
from pygerber.tokens import D03_Token


class D03_TokenText(TestCase):
    def parse_token(self, source):
        re_match = D03_Token.regex.match(source, 0)
        if re_match is not None:
            return D03_Token(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")

    def assertValues(self, token, X, Y):
        self.assertTrue(
            token.X == X and token.Y == Y, f"{token.X} == {X} and {token.Y} == {Y}"
        )

    def test_valid_match(self):
        token = self.parse_token("X1700Y2000D03*")
        self.assertValues(token, 0.0017, 0.002)

    def test_one_arg_missing(self):
        token = self.parse_token("X600000D03*")
        self.assertValues(token, 0.6, None)

    def test_invalid_match(self):
        self.assertRaises(RuntimeError, lambda: self.parse_token("B1700Y2000D03*"))

    def get_renderer_mock(self):
        return Mock(
            draw_flash=Mock(),
            move_pointer=Mock(),
            bbox_flash=Mock(),
        )

    def test_render(self):
        token = self.parse_token("X600000D03*")
        renderer = self.get_renderer_mock()
        token.render(renderer)
        renderer.draw_flash.assert_called_with(token.point)

    def test_post_render(self):
        token = self.parse_token("X600000D03*")
        renderer = self.get_renderer_mock()
        token.post_render(renderer)
        renderer.move_pointer.assert_called_with(token.point)

    def test_bbox(self):
        token = self.parse_token("X600000D03*")
        renderer = self.get_renderer_mock()
        token.bbox(renderer)
        renderer.bbox_flash.assert_called_with(token.point)


if __name__ == "__main__":
    main()
