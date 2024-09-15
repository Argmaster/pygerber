"""`errors` module aggregates all exceptions related to the PillowVirtualMachine."""

from __future__ import annotations

from pygerber.vm.types.errors import VirtualMachineError


class PillowVirtualMachineError(VirtualMachineError):
    """Base class for all exceptions in the PillowVirtualMachine."""


class DPMMTooSmallError(PillowVirtualMachineError):
    """Raised when dots per millimeter is too small for the given DPI."""

    def __init__(self, dpmm: int) -> None:
        super().__init__(
            f"Dots per millimeter ({dpmm}) is to small to render desired image."
        )
        self.dpmm = dpmm
