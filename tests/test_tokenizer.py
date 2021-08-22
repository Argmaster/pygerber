from pygerber.tokens.token import Token
from unittest import TestCase, main
from pygerber.tokenizer import Tokenizer
from .test_meta.test_aperture import ApertureSetTest


class TokenizerTest(TestCase):
    def test_tokenizer_init(self):
        tokenizer = Tokenizer(ApertureSetTest.get_dummy_apertureSet())
        tokenizer.tokenize_string(
            """
            %FSLAX26Y26*%
            %MOMM*%
            %ADD100C,1.5*%
            D100*
            X0Y0D03*
            M02*
            """
        )
        self.assertEqual(tokenizer.token_stack_size, 6)

if __name__ == "__main__":
    main()
