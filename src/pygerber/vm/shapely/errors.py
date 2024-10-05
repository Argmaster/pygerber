"""`errors` module aggregates all exceptions related to the `ShapelyVirtualMachine`."""

from __future__ import annotations

from pygerber.vm.types.errors import VirtualMachineError


class ShapelyVirtualMachineError(VirtualMachineError):
    """Base class for all exceptions in the `ShapelyVirtualMachine`."""


class ShapelyNotInstalledError(ShapelyVirtualMachineError):
    """Raised when shapely package or other dependencies of `ShapelyVirtualMachine`
    are not installed.

    To install all dependencies of `ShapelyVirtualMachine`, run:

    ```bash
    pip install pygerber[shapely]
    ```
    """
