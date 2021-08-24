from pygerber.meta.meta import DrawingMeta
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

    def test_fill_xy_none_with_zero(self):
        DrawingMeta


if __name__ == "__main__":
    main()
