"""Macro primitives tokens."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, List, Optional

from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.point import Point
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from typing_extensions import Self


class Primitive(Expression):
    """Wrapper for macro primitive token, common base class for specialized tokens."""

    symbol: ClassVar[str] = "X"


class PrimitiveCircle(Primitive):
    """Wrapper for macro circle primitive token."""

    symbol: ClassVar[str] = "1"

    exposure: Expression
    diameter: Expression
    center_x: Expression
    center_y: Expression
    rotation: Optional[Expression]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: Expression = unwrap(tokens["exposure"])
        diameter: Expression = unwrap(tokens["diameter"])
        center_x: Expression = unwrap(tokens["center_x"])
        center_y: Expression = unwrap(tokens["center_y"])
        rotation: Optional[Expression] = (
            unwrap(tokens["rotation"]) if tokens.get("rotation") is not None else None
        )

        return cls(
            exposure=exposure,
            diameter=diameter,
            center_x=center_x,
            center_y=center_y,
            rotation=rotation,
        )

    def __str__(self) -> str:
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.diameter}"
        string += f",{self.center_x}"
        string += f",{self.center_y}"

        if self.rotation is not None:
            string += f",{self.rotation}"

        return string + "*"


class PrimitiveVectorLine(Primitive):
    """Wrapper for macro vector line primitive token."""

    symbol: ClassVar[str] = "20"

    exposure: Expression
    width: Expression
    start_x: Expression
    start_y: Expression
    end_x: Expression
    end_y: Expression
    rotation: Expression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: Expression = unwrap(tokens["exposure"])
        width: Expression = unwrap(tokens["width"])
        start_x: Expression = unwrap(tokens["start_x"])
        start_y: Expression = unwrap(tokens["start_y"])
        end_x: Expression = unwrap(tokens["end_x"])
        end_y: Expression = unwrap(tokens["end_y"])
        rotation: Expression = unwrap(tokens["rotation"])

        return cls(
            exposure=exposure,
            width=width,
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            rotation=rotation,
        )

    def __str__(self) -> str:
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.width}"
        string += f",{self.start_x}"
        string += f",{self.start_y}"
        string += f",{self.end_x}"
        string += f",{self.end_y}"
        string += f",{self.rotation}"

        return string + "*"


class PrimitiveCenterLine(Primitive):
    """Wrapper for macro center line primitive token."""

    symbol: ClassVar[str] = "21"

    exposure: Expression
    width: Expression
    hight: Expression
    center_x: Expression
    center_y: Expression
    rotation: Expression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: Expression = unwrap(tokens["exposure"])
        width: Expression = unwrap(tokens["width"])
        hight: Expression = unwrap(tokens["hight"])
        center_x: Expression = unwrap(tokens["center_x"])
        center_y: Expression = unwrap(tokens["center_y"])
        rotation: Expression = unwrap(tokens["rotation"])

        return cls(
            exposure=exposure,
            width=width,
            hight=hight,
            center_x=center_x,
            center_y=center_y,
            rotation=rotation,
        )

    def __str__(self) -> str:
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.width}"
        string += f",{self.hight}"
        string += f",{self.center_x}"
        string += f",{self.center_y}"
        string += f",{self.rotation}"

        return string + "*"


class PrimitiveOutline(Primitive):
    """Wrapper for macro outline primitive token."""

    symbol: ClassVar[str] = "4"

    exposure: Expression
    number_of_vertices: Expression
    start_x: Expression
    start_y: Expression
    rotation: Expression
    point: List[Point]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: Expression = unwrap(tokens["exposure"])
        number_of_vertices: Expression = unwrap(tokens["number_of_vertices"])
        start_x: Expression = unwrap(tokens["start_x"])
        start_y: Expression = unwrap(tokens["start_y"])
        rotation: Expression = unwrap(tokens["rotation"])
        point: list[Point] = list(tokens.get("point", []))

        return cls(
            exposure=exposure,
            number_of_vertices=number_of_vertices,
            start_x=start_x,
            start_y=start_y,
            rotation=rotation,
            point=point,
        )

    def __str__(self) -> str:
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.number_of_vertices}"
        string += f",{self.start_x}"
        string += f",{self.start_y}"
        string += f",{self.rotation}"

        for point in self.point:
            string += f",{point}"

        return string + "*"


class PrimitivePolygon(Primitive):
    """Wrapper for macro outline primitive token."""

    symbol: ClassVar[str] = "5"

    exposure: Expression
    number_of_vertices: Expression
    center_x: Expression
    center_y: Expression
    diameter: Expression
    rotation: Expression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: Expression = unwrap(tokens["exposure"])
        number_of_vertices: Expression = unwrap(tokens["number_of_vertices"])
        center_x: Expression = unwrap(tokens["center_x"])
        center_y: Expression = unwrap(tokens["center_y"])
        diameter: Expression = unwrap(tokens["diameter"])
        rotation: Expression = unwrap(tokens["rotation"])
        return cls(
            exposure=exposure,
            number_of_vertices=number_of_vertices,
            center_x=center_x,
            center_y=center_y,
            diameter=diameter,
            rotation=rotation,
        )

    def __str__(self) -> str:
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.number_of_vertices}"
        string += f",{self.center_x}"
        string += f",{self.center_y}"
        string += f",{self.diameter}"
        string += f",{self.rotation}"

        return string + "*"


class PrimitiveThermal(Primitive):
    """Wrapper for macro outline primitive token."""

    symbol: ClassVar[str] = "7"

    center_x: Expression
    center_y: Expression
    outer_diameter: Expression
    inner_diameter: Expression
    gap: Expression
    rotation: Expression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        center_x: Expression = unwrap(tokens["center_x"])
        center_y: Expression = unwrap(tokens["center_y"])
        outer_diameter: Expression = unwrap(tokens["outer_diameter"])
        inner_diameter: Expression = unwrap(tokens["inner_diameter"])
        gap: Expression = unwrap(tokens["gap"])
        rotation: Expression = unwrap(tokens["rotation"])
        return cls(
            center_x=center_x,
            center_y=center_y,
            outer_diameter=outer_diameter,
            inner_diameter=inner_diameter,
            gap=gap,
            rotation=rotation,
        )

    def __str__(self) -> str:
        string = self.symbol

        string += f",{self.center_x}"
        string += f",{self.center_y}"
        string += f",{self.outer_diameter}"
        string += f",{self.inner_diameter}"
        string += f",{self.gap}"
        string += f",{self.rotation}"

        return string + "*"
