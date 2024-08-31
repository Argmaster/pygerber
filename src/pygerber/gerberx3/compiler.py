"""`pygerber.gerberx3.compiler.compiler` module contains implementation of compiler for
transforming Gerber (AST) to PyGerber rendering VM commands (RVMC).
"""

from __future__ import annotations

from pygerber.gerberx3.ast.nodes import File
from pygerber.gerberx3.ast.state_tracking_visitor import StateTrackingVisitor
from pygerber.vm.commands import Command
from pygerber.vm.rvmc import RVMC


class CommandBuffer:
    """Container for commands and metadata about relations with other containers."""

    def __init__(self) -> None:
        self.commands: list[Command] = []
        self.depends_on: set[str] = set()


class Compiler(StateTrackingVisitor):
    """Compiler for transforming transforming Gerber (AST) to PyGerber rendering VM
    commands (RVMC).
    """

    def __init__(self, *, ignore_program_stop: bool = False) -> None:
        super().__init__(ignore_program_stop=ignore_program_stop)

    def compile(self, ast: File) -> RVMC:
        """Compile Gerber AST to RVMC."""
        self.buffers: dict[str, CommandBuffer] = {}

        ast.visit(self)

        return RVMC([])
