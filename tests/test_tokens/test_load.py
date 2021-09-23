# -*- coding: utf-8 -*-
from unittest import TestCase, main

from pygerber.drawing_state import DrawingState
from pygerber.tokens import (
    LoadMirroringToken,
    LoadPolarityToken,
    LoadRotationToken,
    LoadScalingToken,
)
from pygerber.tokens.load import LoadUnitToken


class TestLoaderTokens(TestCase):
    def parse_token(self, TokenClass, source):
        re_match = TokenClass.regex.match(source, 0)
        if re_match is not None:
            return TokenClass(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")

    def test_LP_token(self):
        token = self.parse_token(LoadPolarityToken, r"%LPD*%")
        self.assertEqual(token.POLARITY, "D")
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.polarity, "D")

    def test_LM_token(self):
        token = self.parse_token(LoadMirroringToken, r"%LMX*%")
        self.assertEqual(token.MIRRORING, "X")
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.mirroring, "X")

    def test_LR_token(self):
        token = self.parse_token(LoadRotationToken, r"%LR45.0*%")
        self.assertEqual(token.ROTATION, 45.0)
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.rotation, 45.0)

    def test_LS_token(self):
        token = self.parse_token(LoadScalingToken, r"%LS0.8*%")
        self.assertEqual(token.SCALE, 0.8)
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.scale, 0.8)

    def test_MOMM_token(self):
        token = self.parse_token(LoadUnitToken, r"%MOMM*%")
        self.assertEqual(token.UNIT, "MM")
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.unit, "MM")

    def test_MOIN_token(self):
        token = self.parse_token(LoadUnitToken, r"%MOIN*%")
        self.assertEqual(token.UNIT, "IN")
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.unit, "IN")


if __name__ == "__main__":
    main()
