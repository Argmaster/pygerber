"""Plot (D01) logic."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class D01Draw(CommandToken):
    """## 4.8.2 Plot (D01).

    Performs a plotting operation, creating a draw or an arc segment. The plot state defines which
    type of segment is created, see 4.7. The syntax depends on the required parameters, and,
    hence, on the plot state.

    D01 creates a linear or circular line segment by plotting from the current point to the
    coordinate pair in the command. Outside a region statement (see 2.3.2) these segments
    are converted to draw or arc objects by stroking them with the current aperture (see 2.3.1).
    Within a region statement these segments form a contour defining a region (see 4.10). The
    effect of D01, e.g. whether a straight or circular segment is created, depends on the
    graphics state (see 2.3.2).

    ### Syntax

    For linear (G01):

    ```ebnf
    D01 = (['X' x_coordinate] ['Y' y_coordinate] 'D01') '*';
    ```

    For Circular (G02|G03)

    ```ebnf
    D01 = (['X' x_coordinate] ['Y' y_coordinate] 'I' x_offset 'J' y-offset ) 'D01' '*';
    ```

    - x_coordinate - `<Coordinate>` is coordinate data - see section 0. It defines the X coordinate of the
        new current point. The default is the X coordinate of the old current point.

    ---

    ## Example

    ```gerber
    X275000Y115000D02*
    G01*
    X2512000Y115000D01*
    G75*
    G03*
    X5005000Y3506000I3000J0D01*
    G01*
    X15752000D01*
    Y12221000D01*
    ```

    ---

    See section 4.8.2 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=83)

    """  # noqa: E501

    def __init__(
        self,
        string: str,
        location: int,
        x: Coordinate,
        y: Coordinate,
        i: Coordinate,
        j: Coordinate,
    ) -> None:
        super().__init__(string, location)
        self.x = x
        self.y = y
        self.i = i
        self.j = j

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        x = tokens.get("x")
        x = Coordinate.new(
            coordinate_type=CoordinateType.X,
            offset=str(x) if x is not None else None,
        )
        y = tokens.get("y")
        y = Coordinate.new(
            coordinate_type=CoordinateType.Y,
            offset=str(y) if y is not None else None,
        )
        i = tokens.get("i")
        i = Coordinate.new(
            coordinate_type=CoordinateType.I,
            offset=str(i) if i is not None else None,
        )
        j = tokens.get("j")
        j = Coordinate.new(
            coordinate_type=CoordinateType.J,
            offset=str(j) if j is not None else None,
        )

        return cls(
            string=string,
            location=location,
            x=x,
            y=y,
            i=i,
            j=j,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().command_draw.pre_parser_visit_token(self, context)
        context.get_hooks().command_draw.on_parser_visit_token(self, context)
        context.get_hooks().command_draw.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        return (
            f"{indent}"
            f"{self.x.get_gerber_code(indent, endline)}"
            f"{self.y.get_gerber_code(indent, endline)}"
            f"{self.i.get_gerber_code(indent, endline)}"
            f"{self.j.get_gerber_code(indent, endline)}"
            "D01"
        )
