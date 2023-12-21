"""Wrapper for G74 token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from pygerber.gerberx3.linter import diagnostic
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class InvalidToken(Token):
    """Invalid syntax.

    This is not a valid Gerber X3/X2 expression.
    """

    def __init__(self, string: str, location: int, content: str) -> None:
        super().__init__(string, location)
        self.content = content

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        content: str = str(tokens["content"])
        return cls(string=string, location=location, content=content)

    def get_token_diagnostics(self) -> Iterable[diagnostic.Diagnostic]:
        """Get diagnostics for this token."""
        yield diagnostic.Diagnostic(
            range=(
                diagnostic.Range(
                    self.get_token_position(),
                    self.get_token_end_position(),
                )
            ),
            message="Invalid syntax.",
            severity=diagnostic.DiagnosticSeverity.Error,
        )

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return self.content
