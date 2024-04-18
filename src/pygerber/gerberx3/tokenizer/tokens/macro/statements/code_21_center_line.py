"""Macro primitive center line."""

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


class Code21CenterLineToken(MacroPrimitiveToken):
    """## 4.5.1.5 Center Line, Code 21.

    A center line primitive is a rectangle defined by its width, height, and center
    point.

    ---

    ## Example

    ```gerber
    %AMRECTANGLE*
    21,1,6.8,1.2,3.4,0.6,30*%
    ```

    ---

    See section 4.5.1.5 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=62)

    """

    symbol: ClassVar[str] = "21"

    def __init__(  # noqa: PLR0913
        self,
        string: str,
        location: int,
        exposure: MacroExpressionToken,
        width: MacroExpressionToken,
        height: MacroExpressionToken,
        center_x: MacroExpressionToken,
        center_y: MacroExpressionToken,
        rotation: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location)
        self.exposure = exposure
        self.width = width
        self.height = height
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        exposure = MacroExpressionToken.ensure_type(tokens["exposure"])
        width = MacroExpressionToken.ensure_type(tokens["width"])
        height = MacroExpressionToken.ensure_type(tokens["height"])
        center_x = MacroExpressionToken.ensure_type(tokens["center_x"])
        center_y = MacroExpressionToken.ensure_type(tokens["center_y"])
        rotation = MacroExpressionToken.ensure_type(tokens["rotation"])

        return cls(
            string=string,
            location=location,
            exposure=exposure,
            width=width,
            height=height,
            center_x=center_x,
            center_y=center_y,
            rotation=rotation,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_code_21_center_line.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_21_center_line.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_21_center_line.post_parser_visit_token(
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
        string += f",{self.height.get_gerber_code(indent, endline)}"
        string += f",{self.center_x.get_gerber_code(indent, endline)}"
        string += f",{self.center_y.get_gerber_code(indent, endline)}"
        string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.exposure}"
        string += f"\n  {self.width}"
        string += f"\n  {self.height}"
        string += f"\n  {self.center_x}"
        string += f"\n  {self.center_y}"
        string += f"\n  {self.rotation}"

        return string
