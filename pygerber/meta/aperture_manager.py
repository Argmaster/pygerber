from pygerber.meta.meta import DrawingMeta
from typing import Dict

from pygerber.exceptions import ApertureSelectionError, InvalidSyntaxError

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
        self.reset_defaults()
        DrawingMeta.__init__(self)

    def reset_defaults(self):
        DrawingMeta.reset_defaults(self)
        self.apertures = {}

    def bind_aperture_set(self, apSet: ApertureSet):
        self.apertureSet = apSet

    def define_aperture(self, type: str, name: str, ID: int, args: object):
        if ID in self.apertures.keys():
            raise InvalidSyntaxError(f"Redefinition of aperture is not allowed. Attempt for aperture D{ID}.")
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
