"""`pygerber.gerberx3.compiler.compiler` module contains implementation of compiler for
transforming Gerber (AST) to PyGerber rendering VM commands (RVMC).
"""

from __future__ import annotations

from pygerber.gerberx3.ast.state_tracking_visitor import StateTrackingVisitor


class Compiler(StateTrackingVisitor):
    """Compiler for transforming transforming Gerber (AST) to PyGerber rendering VM
    commands (RVMC).
    """

    def __init__(self, *, ignore_program_stop: bool = False) -> None:
        super().__init__(ignore_program_stop=ignore_program_stop)
