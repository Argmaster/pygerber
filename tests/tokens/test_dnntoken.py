from unittest import TestCase, main

from pygerber.tokens import D01_Token
from pygerber.meta import Meta


class D01_TokenText(TestCase):
    def test_valid_match_ij(self):
        META = Meta()
        SOURCE = "I300J100D01*"
        dnntoken = D01_Token.match(SOURCE, 0)
        self.assertTrue(dnntoken)
        dnntoken.dispatch(META)
        self.assertEqual(dnntoken.X, None)
        self.assertEqual(dnntoken.Y, None)
        self.assertEqual(dnntoken.I, 0.0003)
        self.assertEqual(dnntoken.J, 0.0001)

    def test_valid_match_xyij(self):
        META = Meta()
        SOURCE = "X-300Y+200I50J50D01*"
        dnntoken = D01_Token.match(SOURCE, 0)
        self.assertTrue(dnntoken)
        dnntoken.dispatch(META)
        self.assertEqual(dnntoken.X, -0.0003)
        self.assertEqual(dnntoken.Y, 0.0002)
        self.assertEqual(dnntoken.I, 0.00005)
        self.assertEqual(dnntoken.J, 0.00005)

    def test_simple_no_match(self):
        SOURCE = "H333I300J100D01*"
        dnntoken = D01_Token.match(SOURCE, 0)
        self.assertFalse(dnntoken)




if __name__ == "__main__":
    main()
