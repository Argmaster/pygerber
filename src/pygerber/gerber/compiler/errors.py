"""`errors` module contains all error classes exclusively raised by Compiler class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.gerber.compiler.compiler import CommandBuffer


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


class MacroNotDefinedError(CompilerError):
    """Raised when macro is not defined in the macro registry."""

    def __init__(self, macro_name: str) -> None:
        super().__init__(f"Macro {macro_name} was not defined before instantiation.")
        self.macro_name = macro_name


class ContourBufferNotSetError(CompilerError):
    """Raised when contour buffer is not set before flushing a contour buffer."""

    def __init__(self) -> None:
        super().__init__(
            "Contour buffer is not set. Set contour buffer before "
            "flushing a contour buffer."
        )
