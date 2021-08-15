from unittest import TestCase, main

from pygerber.tokens import D01_Token
from pygerber.meta import Meta


class D01_TokenText(TestCase):
    def test_simple_valid_match(self):
        META = Meta()
        SOURCE = "I300J100D01*"
        dnntoken = D01_Token.match(SOURCE, 0)


if __name__ == "__main__":
    main()
