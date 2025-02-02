"""`command` module contains the base class for commands executable on PyGerber VMs."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from pydantic import Field

from pygerber.vm.types.model import ModelType

if TYPE_CHECKING:
    from pygerber.vm.vm import CommandVisitor


class Command(ModelType):
    """Base class for drawing commands."""

    metadata: Optional[dict[str, str]] = Field(default=None)

    @abstractmethod
    def visit(self, visitor: CommandVisitor) -> None:
        """Visitor interface implementation."""
