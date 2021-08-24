# -*- coding: utf-8 -*-
from tests.testutils.meta import get_or_create_dummy_meta
from tests.testutils.apertures import ApertureCollector
from pygerber.mathclasses import BoundingBox
from pygerber.meta.meta import Unit
from pygerber.tokens.gnn import G55_Token, G70_Token, G71_Token, G90_Token, G91_Token
from unittest import TestCase, main
from pygerber.tokens import G0N_Token, G36_Token, G37_Token
from pygerber.meta import Meta, Interpolation


class G0N_Token_Test(TestCase):
    def init_token(self, source):
        META = Meta(None)
        token = G0N_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        token.affect_meta()
        return META

    def test_G01(self):
        META = self.init_token("G01*")
        self.assertEqual(META.interpolation, Interpolation.Linear)

    def test_G02(self):
        META = self.init_token("G02*")
        self.assertEqual(META.interpolation, Interpolation.ClockwiseCircular)

    def test_G03(self):
        META = self.init_token("G03*")
        self.assertEqual(META.interpolation, Interpolation.CounterclockwiseCircular)


class GNN_Token_Test(TestCase):
    def init_token(self, source, token_class, meta=None):
        META = get_or_create_dummy_meta(meta)
        token = token_class.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        return token, META

    def test_G36_G37(self):
        token, meta = self.init_token("G36*", G36_Token)
        token.affect_meta()
        self.assertTrue(meta.is_regionmode)
        token, meta = self.init_token("G37*", G37_Token, meta)
        token.affect_meta()
        self.assertFalse(meta.is_regionmode)
        self.assertRaises(ApertureCollector.CalledFinish, token.render)
        self.assertEqual(token.bbox(), BoundingBox(0, 0, 0, 0))

    def test_G70(self):
        token, meta = self.init_token("G70*", G70_Token)
        token.affect_meta()
        self.assertEqual(meta.unit, Unit.INCHES)

    def test_G71(self):
        token, meta = self.init_token("G71*", G71_Token)
        token.affect_meta()
        self.assertEqual(meta.unit, Unit.MILLIMETERS)

    def test_G90(self):
        token, meta = self.init_token("G90*", G90_Token)
        token.affect_meta()
        self.assertEqual(meta.coparser.get_mode(), "A")

    def test_G91(self):
        token, meta = self.init_token("G91*", G91_Token)
        token.affect_meta()
        self.assertEqual(meta.coparser.get_mode(), "I")


if __name__ == "__main__":
    main()
