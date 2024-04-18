"""Macro primitive polygon token."""

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


class Code5PolygonToken(MacroPrimitiveToken):
    """## 4.5.1.7 Polygon, Code 5.

    A polygon primitive is a regular polygon defined by the number of vertices n, the
    center point and the diameter of the circumscribed circle.

    ---

    ## Example

    ```gerber
    %AMPolygon*
    5,1,8,0,0,8,0*%
    ```

    ---

    See section 4.5.1.7 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=65)

    """

    symbol: ClassVar[str] = "5"

    def __init__(  # noqa: PLR0913
        self,
        string: str,
        location: int,
        exposure: MacroExpressionToken,
        number_of_vertices: MacroExpressionToken,
        center_x: MacroExpressionToken,
        center_y: MacroExpressionToken,
        diameter: MacroExpressionToken,
        rotation: MacroExpressionToken,
    ) -> None:
        super().__init__(string, location)
        self.exposure = exposure
        self.number_of_vertices = number_of_vertices
        self.center_x = center_x
        self.center_y = center_y
        self.diameter = diameter
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        exposure = MacroExpressionToken.ensure_type(tokens["exposure"])
        number_of_vertices = MacroExpressionToken.ensure_type(
            tokens["number_of_vertices"],
        )
        center_x = MacroExpressionToken.ensure_type(tokens["center_x"])
        center_y = MacroExpressionToken.ensure_type(tokens["center_y"])
        diameter = MacroExpressionToken.ensure_type(tokens["diameter"])
        rotation = MacroExpressionToken.ensure_type(tokens["rotation"])
        return cls(
            string=string,
            location=location,
            exposure=exposure,
            number_of_vertices=number_of_vertices,
            center_x=center_x,
            center_y=center_y,
            diameter=diameter,
            rotation=rotation,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_code_5_polygon.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_5_polygon.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_5_polygon.post_parser_visit_token(
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
        string += f",{self.number_of_vertices.get_gerber_code(indent, endline)}"
        string += f",{self.center_x.get_gerber_code(indent, endline)}"
        string += f",{self.center_y.get_gerber_code(indent, endline)}"
        string += f",{self.diameter.get_gerber_code(indent, endline)}"
        string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.exposure}"
        string += f"\n  {self.number_of_vertices}"
        string += f"\n  {self.center_x}"
        string += f"\n  {self.center_y}"
        string += f"\n  {self.diameter}"
        string += f"\n  {self.rotation}"

        return string
