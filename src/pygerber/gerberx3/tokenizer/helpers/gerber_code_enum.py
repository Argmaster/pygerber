"""Enum with GerberCode interface implementation."""

from __future__ import annotations

from enum import Enum

from pygerber.gerberx3.tokenizer.tokens.bases.gerber_code import GerberCode


class GerberCodeEnum(GerberCode, Enum):
    """Enum with GerberCode interface implementation."""

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}{self.value}"
