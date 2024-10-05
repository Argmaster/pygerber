"""`types` package contains all utility types used in the `VirtualMachine` ecosystem."""

from __future__ import annotations

from pygerber.vm.types.box import Box
from pygerber.vm.types.color import Color
from pygerber.vm.types.errors import (
    EmptyAutoSizedLayerNotAllowedError,
    LayerAlreadyExistsError,
    LayerNotFoundError,
    NoLayerSetError,
    NoMainLayerError,
    PasteDeferredLayerNotAllowedError,
    VirtualMachineError,
)
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.matrix import Matrix3x3
from pygerber.vm.types.style import Style
from pygerber.vm.types.vector import Vector

__all__ = [
    "Vector",
    "Matrix3x3",
    "Box",
    "LayerID",
    "Color",
    "VirtualMachineError",
    "EmptyAutoSizedLayerNotAllowedError",
    "NoLayerSetError",
    "LayerNotFoundError",
    "LayerAlreadyExistsError",
    "PasteDeferredLayerNotAllowedError",
    "NoMainLayerError",
    "Style",
]
