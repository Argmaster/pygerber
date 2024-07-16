"""Macro statement token."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken


class MacroStatementToken(CommandToken):
    """Wrapper for in-macro expression."""

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}0 {self.__class__.__qualname__} no formatting available"
