"""`rvmc` module contains definition of RVMC class."""

from __future__ import annotations

from typing import Sequence

from pygerber.vm.commands import Command


class RVMC:
    """Container class for PyGerber Rendering Virtual Machine Commands (RVMC)."""

    def __init__(self, commands: Sequence[Command]) -> None:
        self.commands = commands
