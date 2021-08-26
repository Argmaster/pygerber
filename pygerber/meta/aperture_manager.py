from pygerber.meta.meta import DrawingMeta
from typing import Dict

from pygerber.exceptions import ApertureSelectionError

from .aperture import Aperture
from .apertureset import ApertureSet


class ApertureManager(DrawingMeta):
    """
    Remember to call bindApertureSet(apSet) before later usage.
    """

    apertures: Dict[int, Aperture]
    apertureSet: ApertureSet

    def __init__(self, apertureSet: ApertureSet) -> None:
        self.bind_aperture_set(apertureSet)
        DrawingMeta.__init__(self)

    def reset_defaults(self):
        DrawingMeta.reset_defaults(self)

    def bind_aperture_set(self, apSet: ApertureSet):
        self.apertureSet = apSet
        self.apertures = {}

    def define_aperture(self, type: str, name: str, ID: int, args: object):
        if type is not None:
            apertureClass = self.apertureSet.getApertureClass(type)
        else:
            apertureClass = self.apertureSet.getApertureClass(name)
        self.apertures[ID] = apertureClass(args, self)

    def get_aperture(self, id: int) -> Aperture:
        aperture = self.apertures.get(id, None)
        if aperture is None:
            raise ApertureSelectionError(f"Aperture with ID {id} was not defined.")
        return aperture
