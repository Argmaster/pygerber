from pygerber.meta.meta import Interpolation, Polarity
from pygerber.tokens.token import Token
from unittest import TestCase, main
from pygerber.tokenizer import Tokenizer
from .test_meta.test_aperture import ApertureCollector, ApertureSetTest


class TokenizerTest(TestCase):

    SOURCE_0 = """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            M02*
            """

    def test_tokenize_string(self):
        tokenizer = Tokenizer(ApertureSetTest.get_dummy_apertureSet())
        tokenizer.tokenize_string(self.SOURCE_0)
        self.assertEqual(tokenizer.token_stack_size, 6)

    def test_tokenize_file(self):
        tokenizer = Tokenizer(ApertureSetTest.get_dummy_apertureSet())
        tokenizer.tokenize_file("./tests/gerber/s0.grb")
        self.assertEqual(tokenizer.token_stack_size, 17)
        self.assertEqual(tokenizer.meta.polarity, Polarity.DARK)
        self.assertTrue(10 in tokenizer.meta.apertures.keys())
        self.assertEqual(tokenizer.meta.interpolation, Interpolation.Linear)

    def test_tokenize_file_example(self):
        tokenizer = Tokenizer(ApertureSetTest.get_dummy_apertureSet())
        tokenizer.tokenize_file("./examples/board_outline.grb")
        self.assertEqual(tokenizer.token_stack_size, 17)

    def test_render(self):
        tokenizer = Tokenizer(ApertureSetTest.get_dummy_apertureSet())
        stack = tokenizer.tokenize_string(self.SOURCE_0)
        self.assertRaises(ApertureCollector.CalledFlash, tokenizer.render, stack)


if __name__ == "__main__":
    main()
