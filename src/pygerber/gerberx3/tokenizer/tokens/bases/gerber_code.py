"""Base class providing GerberCode interface."""

from __future__ import annotations

from typing import Iterable


class GerberCode:
    """Interface of object which can be converted to gerber code."""

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G04 {self.__class__.__qualname__} no formatting available*"

    def get_gerber_code_one_line_pretty_display(self) -> str:
        """Get gerber code represented by this token."""
        return f"G04 {self.__class__.__qualname__} no formatting available*"


def get_gerber_code(
    tokens: Iterable[GerberCode],
    indent: str = "",
    endline: str = "\n",
) -> str:
    """Get gerber code from iterable of tokens."""
    return endline.join(t.get_gerber_code(indent, endline) for t in tokens)
