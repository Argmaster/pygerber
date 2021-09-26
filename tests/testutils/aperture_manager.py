# -*- coding: utf-8 -*-
from pygerber.renderer.aperture_manager import ApertureManager
from tests.testutils.apertures import get_dummy_apertureSet


def get_dummy_bound_aperture_manager():
    am = ApertureManager(get_dummy_apertureSet(), None)
    return am
