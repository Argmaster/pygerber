# -*- coding: utf-8 -*-
from unittest import TestCase, main

from pygerber.tokens import ADD_Token
from pygerber.meta import Meta


class ADD_TokenTest(TestCase):
    def init_token(self, source):
        META = Meta()
        token = ADD_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        return token, META

    def assertValues(
        self,
        token: ADD_Token,
        ID,
        TYPE,
        *,
        NAME=None,
        X=None,
        Y=None,
        VERTICES=None,
        DIAMETER=None,
        HOLE_DIAMETER=None,
        ROTATION=None,
    ):
        self.assertTrue(token.ID == ID)
        self.assertTrue(token.TYPE == TYPE)
        self.assertTrue(token.NAME == NAME)
        self.assertTrue(token.ARGS.X == X)
        self.assertTrue(token.ARGS.Y == Y)
        self.assertTrue(token.ARGS.VERTICES == VERTICES)
        self.assertTrue(token.ARGS.DIAMETER == DIAMETER)
        self.assertTrue(token.ARGS.HOLE_DIAMETER == HOLE_DIAMETER)
        self.assertTrue(token.ARGS.ROTATION == ROTATION)

    def test_valid_circle(self):
        token, meta = self.init_token(r"%ADD10C,0.1*%")
        self.assertValues(token, 10, "C", DIAMETER=0.1)

    def test_valid_rectangle(self):
        token, meta = self.init_token(r"%ADD12R,0.6X0.6*%")
        self.assertValues(token, 12, "R", X=0.6, Y=0.6)


if __name__ == "__main__":
    main()
