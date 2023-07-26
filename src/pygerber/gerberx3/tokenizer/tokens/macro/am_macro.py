"""Container token for macro definition."""

from __future__ import annotations

from textwrap import indent
from typing import TYPE_CHECKING, Any, List

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.token import Token
from pygerber.sequence_tools import flatten, unwrap

if TYPE_CHECKING:
    from typing_extensions import Self


class MacroDefinition(Token):
    """Container token for macro definition."""

    macro_name: str
    macro_body: List[Expression]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        macro_name: str = tokens["macro_name"]
        macro_body: List[Expression] = [
            unwrap(e) for e in flatten(tokens["macro_body"])
        ]

        return cls(macro_name=macro_name, macro_body=macro_body)

    def __str__(self) -> str:
        str_body = "\n".join(str(e) for e in self.macro_body)
        indented_body = indent(str_body, prefix="  ")
        return f"%AM{self.macro_name}*\n{indented_body}\n%"
