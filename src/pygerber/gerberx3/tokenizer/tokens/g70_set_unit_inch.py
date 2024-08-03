"""Wrapper for G70 token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class SetUnitInch(CommandToken):
    """Wrapper for G70 token.

    Set the `Unit` to inch.

    This historic codes perform a function handled by the MO command. See 4.2.1.
    Sometimes used. Deprecated in 2012

    See section 8.1 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().set_unit_inch.pre_parser_visit_token(self, context)
        context.get_hooks().set_unit_inch.on_parser_visit_token(self, context)
        context.get_hooks().set_unit_inch.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G70"
