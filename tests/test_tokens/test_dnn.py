# -*- coding: utf-8 -*-
from unittest.mock import Mock
from pygerber.drawing_state import DrawingState
from unittest import TestCase, main

from pygerber.tokens import DNN_Loader_Token, DNN_Loader_Token


class DNN_Loader_Token_Test(TestCase):

    def parse_token(self, source):
        re_match = DNN_Loader_Token.regex.match(source, 0)
        if re_match is not None:
            return DNN_Loader_Token(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")

    def test_match(self):
        source = "D12*"
        token = self.parse_token(source)
        self.assertIsNotNone(token)
        self.assertEqual(token.ID, 12)

    def test_invalid_match(self):
        self.assertRaises(RuntimeError, lambda: self.parse_token("D07*"))

    def get_renderer_mock(self):
        return Mock()

    def test_pre_render(self):
        token = self.parse_token("D10*")
        renderer = self.get_renderer_mock()
        token.pre_render(renderer)
        renderer.select_aperture.assert_called_with(10)

if __name__ == "__main__":
    main()
