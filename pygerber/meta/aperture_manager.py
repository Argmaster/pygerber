from typing import Dict

from pygerber.exceptions import ApertureSelectionError
from pygerber.meta.spec import Spec
from pygerber.tokens.add import ADD_Token

from .aperture import Aperture, ApertureSet


class ApertureManager:
    """
    Remember to call bindApertureSet(apSet) before later usage.
    """

    apertures: Dict[int, Aperture]
    apertureSet: ApertureSet

    def __init__(self, apertureSet: ApertureSet) -> None:
        self.bind_aperture_set(apertureSet)

    def bind_aperture_set(self, apSet: ApertureSet):
        self.apertureSet = apSet
        self.apertures = {}

    def define_aperture(self, type: str, name: str, ID: int, args: object):
        if type is not None:
            apertureClass = self.apertureSet.getApertureClass(type)
        else:
            apertureClass = self.apertureSet.getApertureClass(name)
        self.apertures[ID] = apertureClass(args)

    def get_aperture(self, id: int) -> Aperture:
        aperture = self.apertures.get(id, None)
        if aperture is None:
            raise ApertureSelectionError(f"Aperture with ID {id} was not defined.")
        return aperture
