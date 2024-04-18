"""Wrapper for aperture select token."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class StepRepeatBegin(CommandToken):
    """Wrapper for SR begin token.

    Opens an SR statement and starts block accumulation.

    See section 4.10 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(
        self,
        string: str,
        location: int,
        x_repeat: int,
        y_repeat: int,
        x_step: Decimal,
        y_step: Decimal,
    ) -> None:
        super().__init__(string, location)
        self.x_repeat = x_repeat
        self.y_repeat = y_repeat
        self.x_step = x_step
        self.y_step = y_step

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        x_repeat = int(str(tokens.get("x_repeat", "0")))
        y_repeat = int(str(tokens.get("y_repeat", "0")))
        x_step = Decimal(str(tokens.get("x_step", "0")))
        y_step = Decimal(str(tokens.get("y_step", "0")))
        return cls(
            string=string,
            location=location,
            x_repeat=x_repeat,
            y_repeat=y_repeat,
            x_step=x_step,
            y_step=y_step,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().step_repeat_begin.pre_parser_visit_token(self, context)
        context.get_hooks().step_repeat_begin.on_parser_visit_token(self, context)
        context.get_hooks().step_repeat_begin.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"SRX{self.x_repeat}Y{self.y_repeat}I{self.x_step}J{self.y_step}"


class StepRepeatEnd(CommandToken):
    """Wrapper for SR end token.

    Ends step and repeat statement.
    """

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().step_repeat_end.pre_parser_visit_token(self, context)
        context.get_hooks().step_repeat_end.on_parser_visit_token(self, context)
        context.get_hooks().step_repeat_end.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return "SR"
