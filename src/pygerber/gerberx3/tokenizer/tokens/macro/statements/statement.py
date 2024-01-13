"""Macro statement token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext


class MacroStatementToken(CommandToken):
    """Wrapper for in-macro expression."""

    def evaluate(
        self,
        macro_context: MacroContext,
        state: State,
        handle: PrivateApertureHandle,
        /,
    ) -> None:
        """Evaluate macro statement."""

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}0 {self.__class__.__qualname__} no formatting available"
