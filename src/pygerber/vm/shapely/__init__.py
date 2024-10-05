"""The `shapely` package contains concrete implementation of `VirtualMachine` using
Shapely library.
"""

from __future__ import annotations

from pygerber.vm.shapely.errors import (
    ShapelyNotInstalledError,
    ShapelyVirtualMachineError,
)
from pygerber.vm.shapely.vm import (
    ShapelyDeferredLayer,
    ShapelyEagerLayer,
    ShapelyResult,
    ShapelyVirtualMachine,
)

__all__ = [
    "ShapelyVirtualMachine",
    "ShapelyEagerLayer",
    "ShapelyDeferredLayer",
    "ShapelyResult",
    "ShapelyNotInstalledError",
    "ShapelyVirtualMachineError",
]
