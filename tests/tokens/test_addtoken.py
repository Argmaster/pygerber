from unittest import TestCase, main

from pygerber.tokens import ADD_Token
from pygerber.meta import Meta


class ADD_TokenTest(TestCase):
    def init_token(self, source):
        META = Meta()
        dnntoken = ADD_Token.match(source, 0)
        self.assertTrue(dnntoken)
        dnntoken.dispatch(META)
        return dnntoken, META

    def assertValues(
        self,
        token: ADD_Token,
        ID,
        TYPE,
        *,
        NAME="",
        X=0.0,
        Y=0.0,
        VERTICES=0,
        DIAMETER=0.0,
        HOLE_DIAMETER=0.0,
        OUTER_DIAMETER=0.0,
        ROTATION=0.0,
    ):
        self.assertTrue(token.ID == ID)
        self.assertTrue(token.TYPE == TYPE)
        self.assertTrue(token.NAME == NAME)
        self.assertTrue(token.X == X, token.X)
        self.assertTrue(token.Y == Y)
        self.assertTrue(token.VERTICES == VERTICES)
        self.assertTrue(token.DIAMETER == DIAMETER)
        self.assertTrue(token.HOLE_DIAMETER == HOLE_DIAMETER)
        self.assertTrue(token.OUTER_DIAMETER == OUTER_DIAMETER)
        self.assertTrue(token.ROTATION == ROTATION)

    def test_valid_circle(self):
        token, meta = self.init_token(r"%ADD10C,0.1*%")
        self.assertValues(token, 10, "C", DIAMETER=0.1)

    def test_valid_rectangle(self):
        token, meta = self.init_token(r"%ADD12R,0.6X0.6*%")
        self.assertValues(token, 12, "R", X=0.6, Y=0.6)


if __name__ == "__main__":
    main()
