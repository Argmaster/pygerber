from tests.testutils.tokenizer import get_dummy_tokenizer
from tests.testutils.apertures import ApertureCollector, get_dummy_apertureSet
from pygerber.exceptions import InvalidSyntaxError, TokenNotFound
from pygerber.mathclasses import BoundingBox
from pygerber.meta.meta import Interpolation, Polarity
from pygerber.tokens.token import Token
from unittest import TestCase, main
from pygerber.tokenizer import Tokenizer


class TokenizerTest(TestCase):

    SOURCE_0 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            M02*
            """

    SOURCE_1 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            """

    SOURCE_2 = """
        XDD
    """

    def test_tokenize_string(self):
        tokenizer = get_dummy_tokenizer()
        tokenizer.tokenize_string(self.SOURCE_0)
        self.assertEqual(tokenizer.token_stack_size, 6)
        self.assertEqual(tokenizer.bbox.as_tuple(), (-0.75, 0.75, 0.75, -0.75))

    def test_tokenize_string_no_end(self):
        tokenizer = get_dummy_tokenizer()
        self.assertRaises(
            InvalidSyntaxError, lambda: tokenizer.tokenize_string(self.SOURCE_1)
        )

    def test_tokenize_file_invalid_syntax(self):
        tokenizer = get_dummy_tokenizer()
        self.assertRaises(
            InvalidSyntaxError, lambda: tokenizer.tokenize_file("tests\\gerber\\invalid_syntax.grb")
        )

    def test_tokenize_string_token_not_found(self):
        tokenizer = get_dummy_tokenizer()
        self.assertRaises(
            TokenNotFound, lambda: tokenizer.tokenize_string(self.SOURCE_2)
        )

    def test_tokenize_file_0(self):
        tokenizer = get_dummy_tokenizer()
        tokenizer.tokenize_file("./tests/gerber/s0.grb")
        self.assertEqual(tokenizer.token_stack_size, 17)
        self.assertEqual(tokenizer.bbox.as_tuple(), (-0.005, 5.005, 11.005, -0.005))

    def test_tokenize_file_1(self):
        tokenizer = get_dummy_tokenizer()
        tokenizer.tokenize_file("./tests/gerber/s1.grb")
        self.assertEqual(tokenizer.token_stack_size, 47)
        self.assertEqual(
            tokenizer.bbox.as_tuple(),
            (-0.0635, 25.3492, 55.062119999999986, -0.020320000000000005),
        )

    def test_tokenize_file_2(self):
        tokenizer = get_dummy_tokenizer()
        tokenizer.tokenize_file("./tests/gerber/s2.grb")
        self.assertEqual(tokenizer.token_stack_size, 116)
        self.assertEqual(
            tokenizer.bbox.as_tuple(),
            (-0.0635, 25.3492, 55.062119999999986, -0.020320000000000005),
        )

    def test_render(self):
        tokenizer = get_dummy_tokenizer()
        tokenizer.tokenize_string(self.SOURCE_0)
        self.assertRaises(ApertureCollector.CalledFlash, tokenizer.render)

    def test_get_bbox(self):
        tokenizer = get_dummy_tokenizer()
        self.assertEqual(tokenizer.get_bbox(), BoundingBox(0, 0, 0, 0))
        tokenizer.tokenize_string(self.SOURCE_0)
        self.assertEqual(tokenizer.get_bbox(), BoundingBox(-0.75, 0.75, 0.75, -0.75))

if __name__ == "__main__":
    main()
