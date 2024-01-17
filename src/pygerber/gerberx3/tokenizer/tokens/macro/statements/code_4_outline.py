"""Macro primitives tokens."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, List

from pygerber.gerberx3.tokenizer.tokens.macro.expressions.macro_expression import (
    MacroExpressionToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.point import Point
from pygerber.gerberx3.tokenizer.tokens.macro.statements.primitive import (
    MacroPrimitiveToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Code4OutlineToken(MacroPrimitiveToken):
    """## 4.5.1.6 Outline, Code 4.

    An outline primitive is an area defined by its outline or contour. The outline is a
    polygon, consisting of linear segments only, defined by its start vertex and n
    subsequent vertices. The outline must be closed, i.e. the last vertex must be equal
    to the start vertex. The outline must comply with all the requirements of a contour
    according to [4.10.3](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=91).

    The maximum number of vertices is 5000. The purpose of this primitive is to create
    apertures to flash pads with special shapes. The purpose is not to create copper
    pours. Use the region statement for copper pours; see
    [4.10](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=90).

    ---

    ## Example

    ```gerber
    %AMTriangle_30*
    4,1,3,
    1,-1,
    1,1,
    2,1,
    1,-1,
    30*
    %
    ```

    ---

    See section 4.5.1.6 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=63)

    """

    symbol: ClassVar[str] = "4"

    def __init__(  # noqa: PLR0913
        self,
        string: str,
        location: int,
        exposure: MacroExpressionToken,
        number_of_vertices: MacroExpressionToken,
        start_x: MacroExpressionToken,
        start_y: MacroExpressionToken,
        rotation: MacroExpressionToken,
        point: List[Point],
    ) -> None:
        super().__init__(string, location)
        self.exposure = exposure
        self.number_of_vertices = number_of_vertices
        self.start_x = start_x
        self.start_y = start_y
        self.rotation = rotation
        self.point = point

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        exposure = MacroExpressionToken.ensure_type(tokens["exposure"])
        number_of_vertices = MacroExpressionToken.ensure_type(
            tokens["number_of_vertices"],
        )
        start_x = MacroExpressionToken.ensure_type(tokens["start_x"])
        start_y = MacroExpressionToken.ensure_type(tokens["start_y"])
        rotation = MacroExpressionToken.ensure_type(tokens["rotation"])

        p = p if (p := tokens.get("point")) is not None else []
        point = [Point.ensure_type(e) for e in p]

        return cls(
            string=string,
            location=location,
            exposure=exposure,
            number_of_vertices=number_of_vertices,
            start_x=start_x,
            start_y=start_y,
            rotation=rotation,
            point=point,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().macro_code_4_outline.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_4_outline.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().macro_code_4_outline.post_parser_visit_token(
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
        string += f",{self.start_x.get_gerber_code(indent, endline)}"
        string += f",{self.start_y.get_gerber_code(indent, endline)}"

        for point in self.point:
            string += f",{point.get_gerber_code(indent, endline)}"

        string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.exposure}"
        string += f"\n  {self.number_of_vertices}"
        string += f"\n  {self.start_x}"
        string += f"\n  {self.start_y}"

        for point in self.point:
            string += f"\n    {point}"

        string += f"\n  {self.rotation}"

        return string
