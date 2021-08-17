# -*- coding: utf-8 -*-
from unittest import TestCase, main

from pygerber.meta import Meta
from pygerber.tokens import ADD_Token


class ADD_TokenTest(TestCase):
    def init_token(self, source):
        META = Meta()
        token = ADD_Token.match(source, 0)
        self.assertTrue(token)
        token.dispatch(META)
        return token

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
        HOLE_DIAMETER=0.0,
        ROTATION=0.0,
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
        token = self.init_token(r"%ADD10C,0.1*%")
        self.assertValues(token, 10, "C", DIAMETER=0.1)
        token = self.init_token(r"%ADD10C,0.5X0.25*%")
        self.assertValues(token, 10, "C", DIAMETER=0.5, HOLE_DIAMETER=0.25)

    def test_valid_rectangle(self):
        token = self.init_token(r"%ADD12R,0.6X0.6*%")
        self.assertValues(token, 12, "R", X=0.6, Y=0.6)
        token = self.init_token(r"%ADD23R,0.044X0.025X0.019*%")
        self.assertValues(token, 23, "R", X=0.044, Y=0.025, HOLE_DIAMETER=0.019)

    def test_valid_obround(self):
        token = self.init_token(r"%ADD22O,0.046X0.026*%")
        self.assertValues(token, 22, "O", X=0.046, Y=0.026)
        token = self.init_token(r"%ADD22O,0.046X0.026X0.019*%")
        self.assertValues(token, 22, "O", X=0.046, Y=0.026, HOLE_DIAMETER=0.019)

    def test_valid_polygon(self):
        token = self.init_token(r"%ADD17P,.040X6*%")
        self.assertValues(token, 17, "P", DIAMETER=0.040, VERTICES=6)
        token = self.init_token(r"%ADD17P,.040X6X0.0X0.019*%")
        self.assertValues(
            token,
            17,
            "P",
            DIAMETER=0.040,
            VERTICES=6,
            ROTATION=0.0,
            HOLE_DIAMETER=0.019,
        )

    def test_valid_named(self):
        token = self.init_token(r"%ADD19THERMAL80*%")
        self.assertValues(token, 19, None, NAME="THERMAL80")

    def test_stringify(self):
        token = self.init_token(r"%ADD10C,0.1*%")
        self.assertEqual(str(token), r"%ADD10C,0.1*%")
        token = self.init_token(r"%ADD23R,0.044X0.025X0.019*%")
        self.assertEqual(str(token), r"%ADD23R,0.044X0.025X0.019*%")
        token = self.init_token(r"%ADD22O,0.046X0.026X0.019*%")
        self.assertEqual(str(token), r"%ADD22O,0.046X0.026X0.019*%")
        token = self.init_token(r"%ADD17P,.040X6X0.0X0.019*%")
        self.assertEqual(str(token), r"%ADD17P,.040X6X0.0X0.019*%")
        token = self.init_token(r"%ADD19THERMAL80*%")
        self.assertEqual(str(token), r"%ADD19THERMAL80*%")


if __name__ == "__main__":
    main()
