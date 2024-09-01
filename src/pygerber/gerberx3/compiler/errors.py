"""`errors` module contains all error classes exclusively raised by Compiler class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.gerberx3.compiler.compiler import CommandBuffer


class CompilerError(Exception):
    """Base class for all exceptions raised by Compiler class."""


class CyclicBufferDependencyError(CompilerError):
    """Raised when cyclic dependency between buffers is detected."""

    def __init__(
        self, parent_buffer: CommandBuffer, child_buffer: CommandBuffer
    ) -> None:
        super().__init__(
            f"Cyclic dependency between buffers {parent_buffer.id_str} and "
            f"{child_buffer.id_str} detected. Cyclic dependencies are not allowed."
        )
        self.parent_buffer = parent_buffer
        self.child_buffer = child_buffer
