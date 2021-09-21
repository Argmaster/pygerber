# -*- coding: utf-8 -*-
from pygerber.tokens.load import LoadUnitToken
from unittest import TestCase, main
from pygerber.tokens import (
    LoadPolarityToken,
    LoadMirroringToken,
    LoadRotationToken,
    LoadScalingToken,
)
from pygerber.meta import Meta


class TestLoaderTokens(TestCase):
    def init_token(self, TokenClass, source):
        meta = Meta(None)
        token = TokenClass.match(source)
        self.assertTrue(token)
        token.dispatch(meta)
        return token, meta

    def test_LP_token(self):
        token, meta = self.init_token(LoadPolarityToken, r"%LPD*%")
        self.assertEqual(token.POLARITY, "D")
        token.alter_state()
        self.assertEqual(meta.polarity, "D")

    def test_LM_token(self):
        token, meta = self.init_token(LoadMirroringToken, r"%LMX*%")
        self.assertEqual(token.MIRRORING, "X")
        token.alter_state()
        self.assertEqual(meta.mirroring, "X")

    def test_LR_token(self):
        token, meta = self.init_token(LoadRotationToken, r"%LR45.0*%")
        self.assertEqual(token.ROTATION, 45.0)
        token.alter_state()
        self.assertEqual(meta.rotation, 45.0)

    def test_LS_token(self):
        token, meta = self.init_token(LoadScalingToken, r"%LS0.8*%")
        self.assertEqual(token.SCALE, 0.8)
        token.alter_state()
        self.assertEqual(meta.scale, 0.8)

    def test_MOMM_token(self):
        token, meta = self.init_token(LoadUnitToken, r"%MOMM*%")
        self.assertEqual(token.UNIT, "MM")
        token.alter_state()
        self.assertEqual(meta.unit, "MM")

    def test_MOIN_token(self):
        token, meta = self.init_token(LoadUnitToken, r"%MOIN*%")
        self.assertEqual(token.UNIT, "IN")
        token.alter_state()
        self.assertEqual(meta.unit, "IN")


if __name__ == "__main__":
    main()
