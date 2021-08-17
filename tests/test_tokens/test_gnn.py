# -*- coding: utf-8 -*-
from unittest import TestCase, main
from pygerber.tokens import G0N_Token, G36_Token, G37_Token
from pygerber.meta import Meta


class G0N_Token_Test(TestCase):

    def init_token(self, source):
        META = Meta()
        token = G0N_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        token.affect_meta()
        return META

    def test_G01(self):
        META = self.init_token("G01*")
        self.assertEqual(META.interpolation, META.Interpolation.Linear)

    def test_G02(self):
        META = self.init_token("G02*")
        self.assertEqual(META.interpolation, META.Interpolation.ClockwiseCircular)

    def test_G03(self):
        META = self.init_token("G03*")
        self.assertEqual(META.interpolation, META.Interpolation.CounterclockwiseCircular)

class G36_G37_Token_Test(TestCase):

    def init_token(self, source, token_class, meta=None):
        META = Meta() if meta is None else meta
        token = token_class.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        token.affect_meta()
        return META

    def test_G36_G37(self):
        META = self.init_token("G36*", G36_Token)
        self.assertEqual(META.is_regionmode, True)
        self.init_token("G37*", G37_Token, META)
        self.assertEqual(META.is_regionmode, False)


if __name__ == "__main__":
    main()
