

from pygerber.tokenizer import Tokenizer
from tests.testutils.apertures import get_dummy_apertureSet


def get_dummy_tokenizer():
    return Tokenizer(get_dummy_apertureSet())