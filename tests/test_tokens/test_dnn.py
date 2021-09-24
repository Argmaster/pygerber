# -*- coding: utf-8 -*-
from unittest import TestCase, main
from unittest.mock import Mock

from pygerber.drawing_state import DrawingState
from pygerber.tokens import DNN_Loader_Token
from pygerber.tokens.dnn import G54DNN_Loader_Token


class DNN_Loader_Token_Test(TestCase):

    S0 = "D12*"
    V0 = 12
    S1 = "D10*"
    V1 = 10

    def parse_token(self, source):
        re_match = DNN_Loader_Token.regex.match(source, 0)
        if re_match is not None:
            return DNN_Loader_Token(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")

    def test_match(self):
        token = self.parse_token(self.S0)
        self.assertIsNotNone(token)
        self.assertEqual(token.ID, self.V0)

    def test_invalid_match(self):
        self.assertRaises(RuntimeError, lambda: self.parse_token("D07*"))

    def get_renderer_mock(self):
        return Mock()

    def test_pre_render(self):
        token = self.parse_token(self.S1)
        renderer = self.get_renderer_mock()
        token.pre_render(renderer)
        renderer.select_aperture.assert_called_with(self.V1)


class G54DNN_Loader_Token_Test(DNN_Loader_Token_Test):

    S0 = "G54D12*"
    S1 = "G54D10*"

    def parse_token(self, source):
        re_match = G54DNN_Loader_Token.regex.match(source, 0)
        if re_match is not None:
            return G54DNN_Loader_Token(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")


if __name__ == "__main__":
    main()
