"""Macro primitive vector line."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from pygerber.gerberx3.tokenizer.tokens.macro.expressions.macro_expression import (
    MacroExpressionToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.statements.primitive import (
    MacroPrimitiveToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code20VectorLineToken(MacroPrimitiveToken):
    """## 4.5.1.4 Vector Line, Code 20.

    A vector line is a rectangle defined by its line width, start and end points. The
    line ends are rectangular.

    ---

    ## Example

    ```gerber
    %AMLine*
    20,1,0.9,0,0.45,12,0.45,0*
    %
    ```

    ---

    See section 4.5.1.4 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=61)

    """

    symbol: ClassVar[str] = "20"

    def __init__(  # noqa: PLR0913
        self,
        string: str,
        location: int,
        exposure: MacroExpressionToken,
        width: MacroExpressionToken,
        start_x: MacroExpressionToken,
        start_y: MacroExpressionToken,
        end_x: MacroExpressionToken,
        end_y: MacroExpressionToken,
        rotation: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location)
        self.exposure = exposure
        self.width = width
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        exposure = MacroExpressionToken.ensure_type(tokens["exposure"])
        width = MacroExpressionToken.ensure_type(tokens["width"])
        start_x = MacroExpressionToken.ensure_type(tokens["start_x"])
        start_y = MacroExpressionToken.ensure_type(tokens["start_y"])
        end_x = MacroExpressionToken.ensure_type(tokens["end_x"])
        end_y = MacroExpressionToken.ensure_type(tokens["end_y"])
        rotation = MacroExpressionToken.ensure_type(tokens["rotation"])

        return cls(
            string=string,
            location=location,
            exposure=exposure,
            width=width,
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            rotation=rotation,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_code_20_vector_line.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_20_vector_line.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_20_vector_line.post_parser_visit_token(
            self,
            context,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        string = self.symbol

        string += f",{self.exposure.get_gerber_code(indent, endline)}"
        string += f",{self.width.get_gerber_code(indent, endline)}"
        string += f",{self.start_x.get_gerber_code(indent, endline)}"
        string += f",{self.start_y.get_gerber_code(indent, endline)}"
        string += f",{self.end_x.get_gerber_code(indent, endline)}"
        string += f",{self.end_y.get_gerber_code(indent, endline)}"
        string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.exposure}"
        string += f"\n  {self.width}"
        string += f"\n  {self.start_x}"
        string += f"\n  {self.start_y}"
        string += f"\n  {self.end_x}"
        string += f"\n  {self.end_y}"
        string += f"\n  {self.rotation}"

        return string
