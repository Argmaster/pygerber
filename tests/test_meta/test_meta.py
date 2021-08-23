from tests.test_meta.test_broker import DrawingBrokerTest
from unittest import TestCase, main
from pygerber.meta import Meta
from .test_aperture import ApertureSetTest


class TestMeta(TestCase):
    @staticmethod
    def get_filled_meta():
        return DrawingBrokerTest.fill_dummy_apertures(
            Meta(ApertureSetTest.get_dummy_apertureSet())
        )


if __name__ == "__main__":
    main()
