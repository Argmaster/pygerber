"""`errors` module aggregates all generic exceptions related to the VirtualMachine
infrastructure.
"""

from __future__ import annotations


class VirtualMachineError(Exception):
    """Base class for all exceptions in the VirtualMachine infrastructure."""


class NoMainLayerError(VirtualMachineError):
    """Raised when no main layer was created by executing RVMC."""


class EmptyAutoSizedLayerNotAllowedError(VirtualMachineError):
    """Raised when an empty AutoSizedLayer is attempted to be created."""


class NoLayerSetError(VirtualMachineError):
    """Raised when no layer was set prior to drawing shapes."""


class LayerNotFoundError(VirtualMachineError):
    """Raised when layer with given ID was not found during paste operation."""


class LayerAlreadyExistsError(VirtualMachineError):
    """Raised when layer with given ID already exists during create operation."""


class PasteDeferredLayerNotAllowedError(VirtualMachineError):
    """Raised when deferred layer is attempted to be pasted into other layer."""
