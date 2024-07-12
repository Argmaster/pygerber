"""`errors` module aggregates all generic exceptions related to the VirtualMachine
infrastructure.
"""

from __future__ import annotations


class VirtualMachineError(Exception):
    """Base class for all exceptions in the VirtualMachine infrastructure."""
