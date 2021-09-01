# -*- coding: utf-8 -*-
from tests.testutils.meta import get_filled_meta, get_or_create_dummy_meta
from tests.testutils.apertures import ApertureCollector
from unittest import TestCase, main

from pygerber.meta import Meta
from pygerber.tokens import D01_Token, D02_Token, D03_Token, DNN_Loader_Token


class D01_TokenText(TestCase):
    def init_token(self, source):
        META = get_filled_meta()
        token = D01_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        return token

    def assertValues(self, token, X, Y, I, J):
        self.assertTrue(
            token.X == X and token.Y == Y and token.I == I and token.J == J,
            f"{token.X} == {X} and {token.Y} == {Y} and {token.I} == {I} and {token.J} == {J}",
        )

    def test_valid_match_ij_xy(self):
        token = self.init_token("I300J100D01*")
        self.assertValues(token, 0, 0, 0.0003, 0.0001)
        token = self.init_token("X1700Y2000D01*")
        self.assertValues(token, 0.0017, 0.002, 0, 0)
        token = self.init_token("Y500000D01*")
        self.assertValues(token, 0, 0.5, 0, 0)

    def test_valid_match_xyij(self):
        token = self.init_token("X-300Y+200I50J50D01*")
        self.assertValues(token, -0.0003, 0.0002, 0.00005, 0.00005)

    def test_simple_no_match(self):
        SOURCE = "H333I300J100D01*"
        token = D01_Token.match(SOURCE, 0)
        self.assertFalse(token)

    def test_render_line(self):
        token = self.init_token("I300J100D01*")
        token.meta.select_aperture(10)
        self.assertRaises(ApertureCollector.CalledLine, token.render)


class D02_TokenText(TestCase):
    def init_token(self, source):
        META = get_or_create_dummy_meta()
        token = D02_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        return token, META

    def assertValues(self, token, X, Y):
        self.assertTrue(
            token.X == X and token.Y == Y, f"{token.X} == {X} and {token.Y} == {Y}"
        )

    def test_valid_match(self):
        token, meta = self.init_token("X1700Y2000D02*")
        self.assertValues(token, 0.0017, 0.002)
        token, meta = self.init_token("X600000D02*")
        self.assertValues(token, 0.6, 0)

    def test_invalid_match(self):
        token = D02_Token.match("X1700Y2000D01*", 0)
        self.assertFalse(token)


class D03_TokenText(TestCase):
    def init_token(self, source):
        META = get_or_create_dummy_meta()
        token = D03_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        return token, META

    def assertValues(self, token, X, Y):
        self.assertTrue(
            token.X == X and token.Y == Y, f"{token.X} == {X} and {token.Y} == {Y}"
        )

    def test_valid_match(self):
        token, meta = self.init_token("X1700Y2000D03*")
        self.assertValues(token, 0.0017, 0.002)
        token, meta = self.init_token("X600000D03*")
        self.assertValues(token, 0.6, 0)

    def test_invalid_match(self):
        token = D03_Token.match("X1700Y2000D01*", 0)
        self.assertFalse(token)


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
