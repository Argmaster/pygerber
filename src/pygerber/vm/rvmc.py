"""`rvmc` module contains definition of RVMC class."""

from __future__ import annotations

from typing import Any, Sequence

from pydantic import BaseModel, Field

from pygerber.vm.commands import Command


class RVMC(BaseModel):
    """Container class for PyGerber Rendering Virtual Machine Commands (RVMC)."""

    commands: Sequence[Command] = Field(default_factory=list)

    def to_json(self, **kwargs: Any) -> str:
        """Convert RVMC to JSON."""
        return self.model_dump_json(serialize_as_any=True, **kwargs)
