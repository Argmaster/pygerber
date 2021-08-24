

from tests.testutils.broker import fill_dummy_apertures
from tests.testutils.apertures import get_dummy_apertureSet
from pygerber.meta import Meta


def get_or_create_dummy_meta(alt: Meta=None):
    if alt is not None:
        return alt
    else:
        return Meta(get_dummy_apertureSet())

def get_filled_meta():
    return fill_dummy_apertures(
        get_or_create_dummy_meta()
    )