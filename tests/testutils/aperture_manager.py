# -*- coding: utf-8 -*-
from tests.testutils.apertures import get_dummy_apertureSet
from pygerber.renderer.aperture_manager import ApertureManager


def get_dummy_bound_aperture_manager():
    am = ApertureManager(get_dummy_apertureSet(), None)
    return am
