"""Wrapper for aperture select token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class EndRegion(CommandToken):
    """Wrapper for G37 token.

    Ends the region statement.

    See section 4.10 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().end_region.pre_parser_visit_token(self, context)
        context.get_hooks().end_region.on_parser_visit_token(self, context)
        context.get_hooks().end_region.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G37"
