"""`layer_id` module contains definition of `LayerID` class used to identify image
layers in `VirtualMachine` classes.
"""

from __future__ import annotations

from pygerber.vm.types.model import VMModelType


class LayerID(VMModelType):
    """Represents the ID of a layer."""

    id: str

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LayerID):
            return False
        return self.id == other.id
