"""Macro primitives tokens."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, ClassVar, List, Optional

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_constant import NumericConstant
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)
from pygerber.gerberx3.tokenizer.tokens.macro.point import Point

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class Primitive(Expression):
    """Wrapper for macro primitive token, common base class for specialized tokens."""

    symbol: ClassVar[str] = "X"


class PrimitiveCircle(Primitive):
    """## 4.5.1.3 Circle, Code 1.

    A circle primitive is defined by its center point and diameter.

    ---

    ## Example

    ```gerber
    %AMCircle*
    1,1,1.5,0,0,0*%
    ```

    ---

    See section 4.5.1.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=60)

    """

    symbol: ClassVar[str] = "1"

    def __init__(
        self,
        string: str,
        location: int,
        exposure: NumericExpression,
        diameter: NumericExpression,
        center_x: NumericExpression,
        center_y: NumericExpression,
        rotation: NumericExpression,
    ) -> None:
        super().__init__(string, location)
        self.exposure = exposure
        self.diameter = diameter
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        exposure = NumericExpression.ensure_type(tokens["exposure"])
        diameter = NumericExpression.ensure_type(tokens["diameter"])
        center_x = NumericExpression.ensure_type(tokens["center_x"])
        center_y = NumericExpression.ensure_type(tokens["center_y"])

        r = tokens.get("rotation")
        rotation: Optional[NumericExpression] = (
            NumericExpression.ensure_type(r) if r is not None else None
        )
        if rotation is None:
            rotation = NumericConstant(string, location, value=Decimal("0.0"))

        return cls(
            string=string,
            location=location,
            exposure=exposure,
            diameter=diameter,
            center_x=center_x,
            center_y=center_y,
            rotation=rotation,
        )

    def evaluate(
        self,
        macro_context: MacroContext,
        state: State,
        handle: PrivateApertureHandle,
    ) -> None:
        """Evaluate macro expression."""
        self.exposure.evaluate_numeric(macro_context, state)
        self.diameter.evaluate_numeric(macro_context, state)
        self.center_x.evaluate_numeric(macro_context, state)
        self.center_y.evaluate_numeric(macro_context, state)
        self.rotation.evaluate_numeric(macro_context, state)

        return super().evaluate(macro_context, state, handle)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        string = self.symbol

        string += f",{self.exposure.get_gerber_code(indent, endline)}"
        string += f",{self.diameter.get_gerber_code(indent, endline)}"
        string += f",{self.center_x.get_gerber_code(indent, endline)}"
        string += f",{self.center_y.get_gerber_code(indent, endline)}"

        if self.rotation is not None:
            string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.exposure}"
        string += f"\n  {self.diameter}"
        string += f"\n  {self.center_x}"
        string += f"\n  {self.center_y}"

        if self.rotation is not None:
            string += f"\n  {self.rotation}"

        return string


class PrimitiveVectorLine(Primitive):
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
        exposure: NumericExpression,
        width: NumericExpression,
        start_x: NumericExpression,
        start_y: NumericExpression,
        end_x: NumericExpression,
        end_y: NumericExpression,
        rotation: NumericExpression,
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
        exposure = NumericExpression.ensure_type(tokens["exposure"])
        width = NumericExpression.ensure_type(tokens["width"])
        start_x = NumericExpression.ensure_type(tokens["start_x"])
        start_y = NumericExpression.ensure_type(tokens["start_y"])
        end_x = NumericExpression.ensure_type(tokens["end_x"])
        end_y = NumericExpression.ensure_type(tokens["end_y"])
        rotation = NumericExpression.ensure_type(tokens["rotation"])

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


class PrimitiveCenterLine(Primitive):
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
        exposure: NumericExpression,
        width: NumericExpression,
        hight: NumericExpression,
        center_x: NumericExpression,
        center_y: NumericExpression,
        rotation: NumericExpression,
    ) -> None:
        super().__init__(string, location)
        self.exposure = exposure
        self.width = width
        self.hight = hight
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        exposure = NumericExpression.ensure_type(tokens["exposure"])
        width = NumericExpression.ensure_type(tokens["width"])
        hight = NumericExpression.ensure_type(tokens["hight"])
        center_x = NumericExpression.ensure_type(tokens["center_x"])
        center_y = NumericExpression.ensure_type(tokens["center_y"])
        rotation = NumericExpression.ensure_type(tokens["rotation"])

        return cls(
            string=string,
            location=location,
            exposure=exposure,
            width=width,
            hight=hight,
            center_x=center_x,
            center_y=center_y,
            rotation=rotation,
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
        string += f",{self.hight.get_gerber_code(indent, endline)}"
        string += f",{self.center_x.get_gerber_code(indent, endline)}"
        string += f",{self.center_y.get_gerber_code(indent, endline)}"
        string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.exposure}"
        string += f"\n  {self.width}"
        string += f"\n  {self.hight}"
        string += f"\n  {self.center_x}"
        string += f"\n  {self.center_y}"
        string += f"\n  {self.rotation}"

        return string


class PrimitiveOutline(Primitive):
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
        exposure: NumericExpression,
        number_of_vertices: NumericExpression,
        start_x: NumericExpression,
        start_y: NumericExpression,
        rotation: NumericExpression,
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
        exposure = NumericExpression.ensure_type(tokens["exposure"])
        number_of_vertices = NumericExpression.ensure_type(
            tokens["number_of_vertices"],
        )
        start_x = NumericExpression.ensure_type(tokens["start_x"])
        start_y = NumericExpression.ensure_type(tokens["start_y"])
        rotation = NumericExpression.ensure_type(tokens["rotation"])

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


class PrimitivePolygon(Primitive):
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
        exposure: NumericExpression,
        number_of_vertices: NumericExpression,
        center_x: NumericExpression,
        center_y: NumericExpression,
        diameter: NumericExpression,
        rotation: NumericExpression,
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
        exposure = NumericExpression.ensure_type(tokens["exposure"])
        number_of_vertices = NumericExpression.ensure_type(
            tokens["number_of_vertices"],
        )
        center_x = NumericExpression.ensure_type(tokens["center_x"])
        center_y = NumericExpression.ensure_type(tokens["center_y"])
        diameter = NumericExpression.ensure_type(tokens["diameter"])
        rotation = NumericExpression.ensure_type(tokens["rotation"])
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


class PrimitiveThermal(Primitive):
    """## 4.5.1.8 Thermal, Code 7.

    The thermal primitive is a ring (annulus) interrupted by four gaps. Exposure is
    always on.

    ---

    ## Example

    ```gerber
    %AMThermal*
    7,0,0,0.95,0.75,0.175,0.0*%
    ```

    ---

    See section 4.5.1.8 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=66)

    """

    symbol: ClassVar[str] = "7"

    def __init__(  # noqa: PLR0913
        self,
        string: str,
        location: int,
        center_x: NumericExpression,
        center_y: NumericExpression,
        outer_diameter: NumericExpression,
        inner_diameter: NumericExpression,
        gap: NumericExpression,
        rotation: NumericExpression,
    ) -> None:
        super().__init__(string, location)
        self.center_x = center_x
        self.center_y = center_y
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter
        self.gap = gap
        self.rotation = rotation

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Initialize token object."""
        center_x = NumericExpression.ensure_type(tokens["center_x"])
        center_y = NumericExpression.ensure_type(tokens["center_y"])
        outer_diameter = NumericExpression.ensure_type(tokens["outer_diameter"])
        inner_diameter = NumericExpression.ensure_type(tokens["inner_diameter"])
        gap = NumericExpression.ensure_type(tokens["gap"])
        rotation = NumericExpression.ensure_type(tokens["rotation"])

        return cls(
            string,
            location,
            center_x=center_x,
            center_y=center_y,
            outer_diameter=outer_diameter,
            inner_diameter=inner_diameter,
            gap=gap,
            rotation=rotation,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        string = self.symbol

        string += f",{self.center_x.get_gerber_code(indent, endline)}"
        string += f",{self.center_y.get_gerber_code(indent, endline)}"
        string += f",{self.outer_diameter.get_gerber_code(indent, endline)}"
        string += f",{self.inner_diameter.get_gerber_code(indent, endline)}"
        string += f",{self.gap.get_gerber_code(indent, endline)}"
        string += f",{self.rotation.get_gerber_code(indent, endline)}"

        return indent + string

    def __str__(self) -> str:
        string = super().__str__()

        string += f"\n  {self.center_x}"
        string += f"\n  {self.center_y}"
        string += f"\n  {self.outer_diameter}"
        string += f"\n  {self.inner_diameter}"
        string += f"\n  {self.gap}"
        string += f"\n  {self.rotation}"

        return string
