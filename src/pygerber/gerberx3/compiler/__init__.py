"""`compiler` module contains internals of Gerber X3 to RVMC compiler."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.compiler.compiler import Compiler
from pygerber.gerberx3.compiler.errors import CompilerError, CyclicBufferDependencyError

if TYPE_CHECKING:
    from pygerber.vm.rvmc import RVMC

__all__ = ["Compiler", "CompilerError", "CyclicBufferDependencyError"]


def compile(ast: Any, **options: Any) -> RVMC:  # noqa: A001
    """Compile GerberX3 AST to RVMC code."""
    return Compiler(**options).compile(ast)
