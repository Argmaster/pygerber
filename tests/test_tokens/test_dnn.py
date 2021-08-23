# -*- coding: utf-8 -*-
from tests.test_meta.test_broker import DrawingBrokerTest
from tests.test_meta.test_aperture import ApertureCollector
from unittest import TestCase, main

from pygerber.meta import Meta
from pygerber.tokens import D01_Token, D02_Token, D03_Token, DNN_Loader_Token
from tests.test_meta.test_meta import TestMeta


class D01_TokenText(TestCase):
    def init_token(self, source):
        META = TestMeta.get_filled_meta()
        dnntoken = D01_Token.match(source, 0)
        self.assertTrue(dnntoken)
        dnntoken.dispatch(META)
        return dnntoken

    def assertValues(self, token, X, Y, I, J):
        self.assertTrue(token.X == X and token.Y == Y and token.I == I and token.J == J)

    def test_valid_match_ij_xy(self):
        dnntoken = self.init_token("I300J100D01*")
        self.assertValues(dnntoken, None, None, 0.0003, 0.0001)
        dnntoken = self.init_token("X1700Y2000D01*")
        self.assertValues(dnntoken, 0.0017, 0.002, None, None)
        dnntoken = self.init_token("Y500000D01*")
        self.assertValues(dnntoken, None, 0.5, None, None)

    def test_valid_match_xyij(self):
        dnntoken = self.init_token("X-300Y+200I50J50D01*")
        self.assertValues(dnntoken, -0.0003, 0.0002, 0.00005, 0.00005)

    def test_simple_no_match(self):
        SOURCE = "H333I300J100D01*"
        dnntoken = D01_Token.match(SOURCE, 0)
        self.assertFalse(dnntoken)

    def test_render_line(self):
        dnntoken = self.init_token("I300J100D01*")
        dnntoken.meta.select_aperture(10)
        self.assertRaises(ApertureCollector.CalledLine, dnntoken.render)


class D02_TokenText(TestCase):
    def init_token(self, source):
        META = Meta(None)
        dnntoken = D02_Token.match(source, 0)
        self.assertTrue(dnntoken)
        dnntoken.dispatch(META)
        return dnntoken, META

    def assertValues(self, token, X, Y):
        self.assertTrue(token.X == X and token.Y == Y)

    def test_valid_match(self):
        dnntoken, meta = self.init_token("X1700Y2000D02*")
        self.assertValues(dnntoken, 0.0017, 0.002)
        dnntoken, meta = self.init_token("X600000D02*")
        self.assertValues(dnntoken, 0.6, None)

    def test_invalid_match(self):
        dnntoken = D02_Token.match("X1700Y2000D01*", 0)
        self.assertFalse(dnntoken)


class D03_TokenText(TestCase):
    def init_token(self, source):
        META = Meta(None)
        dnntoken = D03_Token.match(source, 0)
        self.assertTrue(dnntoken)
        dnntoken.dispatch(META)
        return dnntoken, META

    def assertValues(self, token, X, Y):
        self.assertTrue(token.X == X and token.Y == Y)

    def test_valid_match(self):
        dnntoken, meta = self.init_token("X1700Y2000D03*")
        self.assertValues(dnntoken, 0.0017, 0.002)
        dnntoken, meta = self.init_token("X600000D03*")
        self.assertValues(dnntoken, 0.6, None)

    def test_invalid_match(self):
        dnntoken = D03_Token.match("X1700Y2000D01*", 0)
        self.assertFalse(dnntoken)


class DNN_Loader_Token_Test(TestCase):
    def test_match(self):
        META = Meta(None)
        source = "D12*"
        token = DNN_Loader_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        self.assertEqual(token.ID, 12)

    def test_fail_on_nn_less_than_10(self):
        META = Meta(None)
        source = "D07*"
        token = DNN_Loader_Token.match(source, 0)
        self.assertFalse(token)


if __name__ == "__main__":
    main()
