"""Container token for macro definition."""

from __future__ import annotations

from textwrap import indent
from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.macro.element import Element
from pygerber.sequence_tools import flatten, unwrap

if TYPE_CHECKING:
    from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression


class MacroDefinition(Element):
    """Container token for macro definition."""

    def __init__(self, macro_name: str, macro_body: list[Expression]) -> None:
        """Initialize token object."""
        super().__init__()
        self.macro_name = macro_name
        self.macro_body = [unwrap(e) for e in flatten(macro_body)]

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        str_body = "\n".join(str(e) for e in self.macro_body)
        indented_body = indent(str_body, prefix="  ")
        return f"%AM{self.macro_name}*\n{indented_body}\n%"
