"""Wrapper for G74 token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from pygerber.gerberx3.linter import diagnostic
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


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
                    start=self.get_token_position(),
                    end=self.get_token_end_position(),
                )
            ),
            message="Invalid syntax.",
            severity=diagnostic.DiagnosticSeverity.Error,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().invalid_token.pre_parser_visit_token(self, context)
        context.get_hooks().invalid_token.on_parser_visit_token(self, context)
        context.get_hooks().invalid_token.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return self.content
