"""`errors` module aggregates all exceptions related to the PillowVirtualMachine."""

from __future__ import annotations

from pygerber.vm.types.errors import VirtualMachineError


class PillowVirtualMachineError(VirtualMachineError):
    """Base class for all exceptions in the PillowVirtualMachine."""


class NoLayerSetError(PillowVirtualMachineError):
    """Raised when no layer was set prior to drawing polygon."""


class BoxNotSetError(PillowVirtualMachineError):
    """Raised when main box was set prior to drawing polygon."""
