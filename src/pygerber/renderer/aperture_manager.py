# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from pygerber.exceptions import ApertureSelectionError, InvalidSyntaxError

if TYPE_CHECKING:
    from pygerber.renderer import Renderer

    from .aperture import Aperture
    from .apertureset import ApertureSet


class ApertureManager:

    apertures: Dict[int, Aperture]
    apertureSet: ApertureSet
    renderer: Renderer
    current_aperture: Aperture = None

    def __init__(self, apertureSet: ApertureSet, renderer: Renderer) -> None:
        self.renderer = renderer
        self.__bind_aperture_set(apertureSet)
        self.set_defaults()

    def __getitem__(self, id: int) -> Aperture:
        return self.apertures.get(id)

    def select_aperture(self, id: int):
        self.current_aperture = self.apertures.get(id)

    def get_current_aperture(self):
        if self.current_aperture is None:
            raise ApertureSelectionError(
                "Attempt to perform operation with aperture without preceding aperture selection."
            )
        return self.current_aperture

    def set_defaults(self):
        self.apertures = {}

    def __bind_aperture_set(self, apSet: ApertureSet):
        self.apertureSet = apSet

    def define_aperture(self, type: str, name: str, ID: int, args: object):
        if ID in self.apertures.keys():
            raise InvalidSyntaxError(
                f"Redefinition of aperture is not allowed. Attempt for aperture D{ID}."
            )
        if type is not None:
            apertureClass = self.apertureSet.getApertureClass(type)
        else:
            apertureClass = self.apertureSet.getApertureClass(name)
        self.apertures[ID] = apertureClass(args, self.renderer)

    def get_aperture(self, id: int) -> Aperture:
        aperture = self.apertures.get(id, None)
        if aperture is None:
            raise ApertureSelectionError(f"Aperture with ID {id} was not defined.")
        return aperture

    def getApertureClass(self, name: str = None, is_region: bool = False):
        return self.apertureSet.getApertureClass(name, is_region)
