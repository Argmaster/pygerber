from typing import Dict, List, Tuple

from pygerber.exceptions import ApertureSelectionError
from pygerber.meta.spec import Spec
from pygerber.tokens.add import ADD_Token

from .aperture import Aperture, ApertureSet


class ApertureManager:
    apertures: Dict[int, Aperture]
    apertureSet: ApertureSet
    region_bounds: List[Tuple[Aperture, Spec]]

    def bindApertureSet(self, apSet: ApertureSet):
        self.apertureSet = apSet

    def defineAperture(self, token: ADD_Token):
        if token.TYPE is not None:
            apertureClass = self.apertureSet.getApertureClass(token.TYPE)
        else:
            apertureClass = self.apertureSet.getApertureClass(token.NAME)
        self.apertures[token.ID] = apertureClass(token.ARGS)

    def selectAperture(self, id: int):
        new_aperture = self.apertures.get(id, None)
        if new_aperture is None:
            raise ApertureSelectionError(f"Aperture with ID {id} was not defined.")
        else:
            self.current_aperture = new_aperture

    def pushRegionStep(self, spec: Spec):
        self.region_bounds.append((self.current_aperture, spec))
